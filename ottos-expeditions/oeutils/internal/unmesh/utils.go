package unmesh

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"text/template"

	"gopkg.in/yaml.v3"

	"github.com/ascend-io/ascend-community-internal/oeutils/internal/logger"
)

// fileCopyStrategy abstracts how individual files are copied from the source
// mesh project into a per‑data‑plane project.  Most files are copied verbatim
// (handled by `copyFile`) but some, such as README.md, require bespoke
// processing.
type fileCopyStrategy func(srcPath, dstPath, dataPlane string) error

// findReplaceVaultNames anonymises vault references so that the resulting
// project can be shared publicly. Any token present in `vaultNames` is replaced
// with the generic placeholder "environment".
func findReplaceVaultNames(codeString string) string {
	for _, vaultName := range vaultNames {
		// Use regexp to replace all occurrences regardless of word boundaries.
		codeString = regexp.MustCompile(regexp.QuoteMeta(vaultName)).ReplaceAllString(codeString, "environment")
	}
	return codeString
}

// projectCopyStrategy performs project YAML processing before writing it to
// the destination. It keeps only relevant parameters and defaults for the dataPlane.
func projectCopyStrategy(srcPath, dstPath, dataPlane string) error {
	logger.Logger.Printf("Processing project YAML: %s to %s for data plane: %s", srcPath, dstPath, dataPlane)
	data, err := os.ReadFile(srcPath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %w", srcPath, err)
	}
	var root yaml.Node
	if err := yaml.Unmarshal(data, &root); err != nil {
		return fmt.Errorf("error parsing YAML: %w", err)
	}
	if root.Kind != yaml.DocumentNode || len(root.Content) == 0 || root.Content[0].Kind != yaml.MappingNode {
		return fmt.Errorf("unexpected YAML structure for %s", srcPath)
	}
	rootMapping := root.Content[0]
	var projectNode *yaml.Node
	for i := 0; i < len(rootMapping.Content); i += 2 {
		if rootMapping.Content[i].Value == "project" {
			projectNode = rootMapping.Content[i+1]
			break
		}
	}
	if projectNode == nil || projectNode.Kind != yaml.MappingNode {
		return fmt.Errorf("project node not found or invalid in %s", srcPath)
	}
	connName := dataPlaneConnName[dataPlane]
	newProject := &yaml.Node{Kind: yaml.MappingNode}
	for i := 0; i < len(projectNode.Content); i += 2 {
		keyNode := projectNode.Content[i]
		valNode := projectNode.Content[i+1]
		switch keyNode.Value {
		case "name", "pip_packages":
			newProject.Content = append(newProject.Content, keyNode, valNode)
		case "parameters":
			if valNode.Kind == yaml.MappingNode {
				newParams := &yaml.Node{Kind: yaml.MappingNode}
				for j := 0; j < len(valNode.Content); j += 2 {
					pKey := valNode.Content[j]
					pVal := valNode.Content[j+1]
					if pKey.Value == "data_planes" && pVal.Kind == yaml.MappingNode {
						newDP := &yaml.Node{Kind: yaml.MappingNode}
						for k := 0; k < len(pVal.Content); k += 2 {
							dpKey := pVal.Content[k]
							dpVal := pVal.Content[k+1]
							if dpKey.Value == dataPlane {
								newDP.Content = append(newDP.Content, dpKey, dpVal)
							}
						}
						newParams.Content = append(newParams.Content, pKey, newDP)
					}
				}
				newProject.Content = append(newProject.Content, keyNode, newParams)
			}
		case "defaults":
			if valNode.Kind == yaml.SequenceNode {
				newDefaults := &yaml.Node{Kind: yaml.SequenceNode}
				for _, item := range valNode.Content {
					if item.Kind != yaml.MappingNode {
						continue
					}
					var itemConn string
					var regexNode *yaml.Node
					for a := 0; a < len(item.Content); a += 2 {
						k := item.Content[a]
						v := item.Content[a+1]
						if k.Value == "spec" && v.Kind == yaml.MappingNode {
							for b := 0; b < len(v.Content); b += 2 {
								if v.Content[b].Value == "data_plane" && v.Content[b+1].Kind == yaml.MappingNode {
									dp := v.Content[b+1]
									for c := 0; c < len(dp.Content); c += 2 {
										if dp.Content[c].Value == "connection_name" {
											itemConn = dp.Content[c+1].Value
										}
									}
								}
							}
						}
						if k.Value == "name" && v.Kind == yaml.MappingNode {
							for d := 0; d < len(v.Content); d += 2 {
								if v.Content[d].Value == "regex" {
									regexNode = v.Content[d+1]
								}
							}
						}
					}
					if itemConn == connName {
						if regexNode != nil {
							regexNode.Value = findReplaceDataPlane(regexNode.Value, dataPlane)
						}
						newDefaults.Content = append(newDefaults.Content, item)
					}
				}
				newProject.Content = append(newProject.Content, keyNode, newDefaults)
			}
		}
	}
	newRoot := &yaml.Node{Kind: yaml.DocumentNode}
	mapping := &yaml.Node{Kind: yaml.MappingNode}
	mapping.Content = []*yaml.Node{
		{Kind: yaml.ScalarNode, Value: "project"},
		newProject,
	}
	newRoot.Content = []*yaml.Node{mapping}
	var buf bytes.Buffer
	enc := yaml.NewEncoder(&buf)
	enc.SetIndent(2)
	if err := enc.Encode(newRoot); err != nil {
		return fmt.Errorf("error marshaling YAML: %w", err)
	}
	enc.Close()
	if err := os.WriteFile(dstPath, buf.Bytes(), 0o644); err != nil {
		return fmt.Errorf("error writing file %s: %w", dstPath, err)
	}
	return nil
}

// findReplaceDataPlaneFlowRef removes the data‑plane suffix from a flow
// reference (e.g. "extract-load-bigquery" -> "extract-load").
//
// The function is intentionally conservative: it short‑circuits if either the
// input string or the data plane is empty to avoid accidental replacements.
func findReplaceDataPlaneFlowRef(codeString, dataPlane string) string {
	if codeString == "" || dataPlane == "" {
		return codeString
	}

	pattern := fmt.Sprintf(`(flow\s*=\s*["'])([^"']*)-(%s)(["'])`, regexp.QuoteMeta(dataPlane))
	re := regexp.MustCompile(pattern)
	result := re.ReplaceAllString(codeString, "$1$2$4")

	return result
}

// findReplaceDataPlane strips the trailing "-<dataPlane>" suffix from any token
// inside `codeString`.
func findReplaceDataPlane(codeString, dataPlane string) string {
	if codeString == "" || dataPlane == "" {
		return codeString
	}

	pattern := fmt.Sprintf(`([^"'\s]+)-(%s)`, regexp.QuoteMeta(dataPlane))
	re := regexp.MustCompile(pattern)
	result := re.ReplaceAllString(codeString, "$1")

	return result
}

func removeDirectory(path string) error {
	if _, err := os.Stat(path); err == nil {
		logger.Logger.Printf("Removing existing directory: %s", path)
		return os.RemoveAll(path)
	}
	return nil
}

func createDirectory(path string) error {
	logger.Logger.Printf("Creating directory: %s", path)
	return os.MkdirAll(path, 0o755)
}

func copyFile(src, dst string) error {
	logger.Logger.Printf("Copying file: %s to %s", src, dst)

	data, err := os.ReadFile(src)
	if err != nil {
		return fmt.Errorf("error reading file %s: %w", src, err)
	}

	if err := os.MkdirAll(filepath.Dir(dst), 0o755); err != nil {
		return fmt.Errorf("error creating destination directory %s: %w", filepath.Dir(dst), err)
	}

	return os.WriteFile(dst, data, 0o644)
}

func copyDirectory(src, dst string) error {
	logger.Logger.Printf("Copying directory: %s to %s", src, dst)

	if err := os.MkdirAll(dst, 0o755); err != nil {
		return fmt.Errorf("error creating directory %s: %v", dst, err)
	}

	entries, err := os.ReadDir(src)
	if err != nil {
		return fmt.Errorf("error reading directory %s: %v", src, err)
	}

	for _, entry := range entries {
		srcPath := filepath.Join(src, entry.Name())
		dstPath := filepath.Join(dst, entry.Name())

		if entry.IsDir() {
			if err := copyDirectory(srcPath, dstPath); err != nil {
				return err
			}
		} else {
			if err := copyFile(srcPath, dstPath); err != nil {
				return err
			}
		}
	}

	return nil
}

// CopyDirectory is an exported wrapper around copyDirectory so that other
// internal packages (e.g. release) can reuse the implementation.
func CopyDirectory(src, dst string) error { return copyDirectory(src, dst) }

// Replace "Data Plane" and "data-plane" in README.md with the correct data plane name
// stripInternalSection removes everything from the "## Internal" header to the
// end of the README. The header is assumed to be the final H2 section used only
// for internal documentation.
func stripInternalSection(content string) string {
	re := regexp.MustCompile(`(?m)^## Internal[\s\S]*$`)
	return re.ReplaceAllString(content, "")
}

// replaceReadmeTemplates injects the correct data‑plane name into the README
// and removes internal‑only sections.
// readmeTemplateData is the data passed to the README Go template.
type readmeTemplateData struct {
	DataPlane      string // Title‑cased display name, e.g. "BigQuery"
	DataPlaneLower string // Lower‑case name, e.g. "bigquery"
}

func replaceReadmeTemplates(content, dataPlane string) string {
	displayName, ok := dataPlaneMap[dataPlane]
	if !ok {
		displayName = dataPlane // fallback
	}

	// Attempt to parse the content as a Go template.  If parsing fails we fall
	// back to the legacy placeholder replacement to maintain backward
	// compatibility with existing READMEs that haven't yet been templatised.
	tmpl, err := template.New("readme").Option("missingkey=default").Parse(content)
	if err != nil {
		logger.Logger.Printf("README is not a valid template, falling back to string replacement: %v", err)
		content = strings.ReplaceAll(content, "Data Plane", displayName)
		content = strings.ReplaceAll(content, "data-plane", strings.ToLower(displayName))
		return stripInternalSection(content)
	}

	var buf bytes.Buffer
	data := readmeTemplateData{DataPlane: displayName, DataPlaneLower: strings.ToLower(displayName)}
	if err := tmpl.Execute(&buf, data); err != nil {
		logger.Logger.Printf("unable to execute README template, falling back to string replacement: %v", err)
		content = strings.ReplaceAll(content, "Data Plane", displayName)
		content = strings.ReplaceAll(content, "data-plane", strings.ToLower(displayName))
		return stripInternalSection(content)
	}

	return stripInternalSection(buf.String())
}

// readmeCopyStrategy performs README‑specific processing before writing it to
// the destination.
func readmeCopyStrategy(srcPath, dstPath, dataPlane string) error {
	data, err := os.ReadFile(srcPath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %w", srcPath, err)
	}

	if err := os.MkdirAll(filepath.Dir(dstPath), 0o755); err != nil {
		return fmt.Errorf("error creating destination directory %s: %w", filepath.Dir(dstPath), err)
	}

	modified := replaceReadmeTemplates(string(data), dataPlane)
	return os.WriteFile(dstPath, []byte(modified), 0o644)
}

// customFileCopyStrategies lists all files that need bespoke processing when
// copied. Any entry not present in this map is copied verbatim using
// `copyFile`.
var customFileCopyStrategies = map[string]fileCopyStrategy{
	"README.md":           readmeCopyStrategy,
	"ascend_project.yaml": projectCopyStrategy,
}

// copyRawFiles copies each file from `rawCopyFiles` into the target project.
// If a custom strategy exists the strategy is invoked, otherwise a simple
// byte‑for‑byte copy is performed.
func copyRawFiles(sourceDir, destDir, dataPlane string) error {
	processed := make(map[string]struct{})

	// First process the explicitly listed raw copy files.
	for _, file := range rawCopyFiles {
		srcPath := filepath.Join(sourceDir, file)
		dstPath := filepath.Join(destDir, file)

		if _, err := os.Stat(srcPath); os.IsNotExist(err) {
			logger.Logger.Printf("Warning: Source file does not exist: %s", srcPath)
			continue
		}

		if strategy, ok := customFileCopyStrategies[file]; ok {
			if err := strategy(srcPath, dstPath, dataPlane); err != nil {
				return err
			}
			continue
		}

		if err := copyFile(srcPath, dstPath); err != nil {
			return err
		}

		// Record that we have handled this file so that we don't process it
		// again in the custom‑file pass below.
		processed[file] = struct{}{}
	}

	// Process any additional files that have custom copy strategies but were
	// not part of rawCopyFiles (e.g. README.md).
	for file, strategy := range customFileCopyStrategies {
		if _, done := processed[file]; done {
			continue // already handled above
		}

		srcPath := filepath.Join(sourceDir, file)
		dstPath := filepath.Join(destDir, file)

		if _, err := os.Stat(srcPath); os.IsNotExist(err) {
			logger.Logger.Printf("Warning: Source file does not exist: %s", srcPath)
			continue
		}

		if err := strategy(srcPath, dstPath, dataPlane); err != nil {
			return err
		}
	}

	return nil
}

func copyRawDirs(sourceDir, destDir string) error {
	for _, dir := range rawCopyDirs {
		srcPath := filepath.Join(sourceDir, dir)
		dstPath := filepath.Join(destDir, dir)

		if _, err := os.Stat(srcPath); os.IsNotExist(err) {
			logger.Logger.Printf("Warning: Source directory does not exist: %s", srcPath)
			continue
		}

		if err := copyDirectory(srcPath, dstPath); err != nil {
			return err
		}
	}

	return nil
}
