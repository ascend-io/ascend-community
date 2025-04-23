package unmesh

// WARNING: sloppy af

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/ascend-io/ascend-community-internal/oeutils/internal/logger"
	"gopkg.in/yaml.v3"
)

const yamlIndent = 2

const (
	envWorkspace   = "WORKSPACE"
	envDevelopment = "DEVELOPMENT"
	envStaging     = "STAGING"
	envProduction  = "PRODUCTION"
)

// --- BEGIN CONFIGURATION ---

// Parameter keys to keep for each data plane
var dataPlaneParamKeys = map[string][]string{
	"bigquery":   {"gcp", "bigquery"},
	"databricks": {"databricks"},
	"snowflake":  {"snowflake"},
}

// Connection name for each data plane
var dataPlaneConnName = map[string]string{
	"bigquery":   "data_plane_bigquery",
	"databricks": "data_plane_databricks",
	"snowflake":  "data_plane_snowflake",
}

// Placeholders for each data plane and parameter
var placeholderConfig = map[string]map[string]map[string]string{
	"bigquery": {
		"gcp": {
			"project_id": "<your-gcp-project-id>",
		},
		"bigquery": {
			"dataset": "OTTOS_EXPEDITIONS_WORKSPACE_<your-name>", // workspace only
		},
	},
	"databricks": {
		"databricks": {
			"workspace_url":       "<your-databricks-workspace-url>",
			"client_id":           "<your-databricks-client-id>",
			"cluster_id":          "<your-databricks-cluster-id>",
			"cluster_http_path":   "<your-databricks-cluster-http-path>",
			"warehouse_http_path": "<your-databricks-warehouse-http-path>",
			"catalog":             "OTTOS_EXPEDITIONS_WORKSPACE_<your-name>", // workspace only
		},
	},
	"snowflake": {
		"snowflake": {
			"account":                "<your-snowflake-account>",
			"user":                   "<your-snowflake-user>",
			"role":                   "<your-snowflake-role>",
			"warehouse":              "<your-snowflake-warehouse>",
			"database":               "OTTOS_EXPEDITIONS_WORKSPACE_<your-name>", // workspace only
			"schema":                 "DEFAULT",
			"max_concurrent_queries": "20",
		},
	},
}

// Parameters to always leave as-is for deployments (per data plane)
var deploymentExceptions = map[string]map[string][]string{
	"bigquery": {
		"bigquery": {"dataset"},
	},
	"databricks": {
		"databricks": {"catalog", "schema"},
	},
	"snowflake": {
		"snowflake": {"database", "schema", "max_concurrent_queries"},
	},
}

// --- END CONFIGURATION ---

// Helper: returns true if the file is a workspace template
func isWorkspaceTemplate(path string) bool {
	return strings.Contains(path, "workspace_template")
}

// Helper: returns true if the file is a deployment YAML
func isDeploymentProfile(path string) bool {
	return strings.Contains(path, "deployment_")
}

// getEnvFromPath returns the deployment environment based on the file path.
func getEnvFromPath(path string) string {
	if strings.Contains(path, "development") {
		return envDevelopment
	} else if strings.Contains(path, "staging") {
		return envStaging
	} else if strings.Contains(path, "production") {
		return envProduction
	}
	return envWorkspace
}

// newYAMLScalar returns a new YAML scalar node.
func newYAMLScalar(val string) *yaml.Node {
	return &yaml.Node{Kind: yaml.ScalarNode, Value: val}
}

// newYAMLMapping returns a new YAML mapping node.
func newYAMLMapping(pairs ...*yaml.Node) *yaml.Node {
	return &yaml.Node{Kind: yaml.MappingNode, Content: pairs}
}

// Helper: set placeholders for parameters according to all data planes and file type
func setAllParameterPlaceholders(params *yaml.Node, isWorkspace bool) {
	for i := 0; i < len(params.Content); i += 2 {
		k, v := params.Content[i], params.Content[i+1]
		for dataPlane, subConfigs := range placeholderConfig {
			if subPlaceholders, ok := subConfigs[k.Value]; ok {
				for j := 0; j < len(v.Content); j += 2 {
					paramKey := v.Content[j].Value
					if isWorkspace {
						if ph, ok := subPlaceholders[paramKey]; ok {
							v.Content[j+1].Value = ph
						}
					} else {
						exceptions := deploymentExceptions[dataPlane][k.Value]
						isException := false
						for _, ex := range exceptions {
							if ex == paramKey {
								isException = true
								break
							}
						}
						if !isException {
							if ph, ok := subPlaceholders[paramKey]; ok {
								v.Content[j+1].Value = ph
							}
						}
					}
				}
			}
		}
	}
}

// makeSnowflakeDeploymentParams returns a YAML node for snowflake deployment parameters.
func makeSnowflakeDeploymentParams(env string) *yaml.Node {
	return newYAMLMapping(
		newYAMLScalar("snowflake"),
		newYAMLMapping(
			newYAMLScalar("account"), newYAMLScalar("<your-snowflake-account>"),
			newYAMLScalar("user"), newYAMLScalar("<your-snowflake-user>"),
			newYAMLScalar("role"), newYAMLScalar("<your-snowflake-role>"),
			newYAMLScalar("warehouse"), newYAMLScalar("<your-snowflake-warehouse>"),
			newYAMLScalar("database"), newYAMLScalar("OTTOS_EXPEDITIONS_"+env),
			newYAMLScalar("schema"), newYAMLScalar("DEFAULT"),
			newYAMLScalar("max_concurrent_queries"), newYAMLScalar("20"),
		),
	)
}

func filterParametersForDataPlane(params *yaml.Node, dataPlane string) *yaml.Node {
	filtered := &yaml.Node{Kind: yaml.MappingNode}
	for _, keepKey := range dataPlaneParamKeys[dataPlane] {
		for j := 0; j < len(params.Content); j += 2 {
			pk, pv := params.Content[j], params.Content[j+1]
			if pk.Value == keepKey {
				filtered.Content = append(filtered.Content, pk, pv)
			}
		}
	}
	return filtered
}

func processProfileFile(srcPath string, dstPath string, dataPlane string) error {
	data, err := os.ReadFile(srcPath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %v", srcPath, err)
	}

	cfgConnName := dataPlaneConnName[dataPlane]

	var root yaml.Node
	if err := yaml.Unmarshal(data, &root); err != nil {
		return fmt.Errorf("error parsing YAML: %v", err)
	}

	// Find the 'profile' mapping node
	var profileNode *yaml.Node
	if root.Kind == yaml.DocumentNode && len(root.Content) > 0 && root.Content[0].Kind == yaml.MappingNode {
		for i := 0; i < len(root.Content[0].Content); i += 2 {
			k := root.Content[0].Content[i]
			if k.Value == "profile" {
				profileNode = root.Content[0].Content[i+1]
				break
			}
		}
	}
	if profileNode == nil {
		return fmt.Errorf("profile node not found in YAML")
	}

	isWorkspace := isWorkspaceTemplate(srcPath)

	// Prepare new ordered profile mapping: parameters first, then defaults
	newProfile := &yaml.Node{Kind: yaml.MappingNode}

	// 1. parameters
	for i := 0; i < len(profileNode.Content); i += 2 {
		k, v := profileNode.Content[i], profileNode.Content[i+1]
		if k.Value == "parameters" {
			if isWorkspace {
				setAllParameterPlaceholders(v, true)
				newProfile.Content = append(newProfile.Content, k, filterParametersForDataPlane(v, dataPlane))
			} else if dataPlane == "snowflake" {
				newProfile.Content = append(newProfile.Content, k, makeSnowflakeDeploymentParams(getEnvFromPath(srcPath)))
			} else {
				setAllParameterPlaceholders(v, false)
				newProfile.Content = append(newProfile.Content, k, filterParametersForDataPlane(v, dataPlane))
			}
		}
	}

	// 2. defaults
	for i := 0; i < len(profileNode.Content); i += 2 {
		k, v := profileNode.Content[i], profileNode.Content[i+1]
		if k.Value == "defaults" {
			filtered := &yaml.Node{Kind: yaml.SequenceNode}
			for _, d := range v.Content {
				if d.Kind != yaml.MappingNode {
					continue
				}
				var connName string
				var regexNode *yaml.Node
				for di := 0; di < len(d.Content); di += 2 {
					if d.Content[di].Value == "spec" {
						spec := d.Content[di+1]
						for si := 0; si < len(spec.Content); si += 2 {
							if spec.Content[si].Value == "data_plane" {
								dp := spec.Content[si+1]
								for dpi := 0; dpi < len(dp.Content); dpi += 2 {
									if dp.Content[dpi].Value == "connection_name" {
										connName = dp.Content[dpi+1].Value
									}
								}
							}
						}
					}
					if d.Content[di].Value == "name" {
						nameNode := d.Content[di+1]
						for ni := 0; ni < len(nameNode.Content); ni += 2 {
							if nameNode.Content[ni].Value == "regex" {
								regexNode = nameNode.Content[ni+1]
							}
						}
					}
				}
				if connName == cfgConnName {
					// Remove -<data-plane> from regex if present
					if regexNode != nil {
						regexNode.Value = findReplaceDataPlane(regexNode.Value, dataPlane)
					}
					filtered.Content = append(filtered.Content, d)
				}
			}
			newProfile.Content = append(newProfile.Content, k, filtered)
		}
	}

	// Marshal the new YAML
	outRoot := &yaml.Node{Kind: yaml.DocumentNode, Content: []*yaml.Node{
		{
			Kind: yaml.MappingNode,
			Content: []*yaml.Node{
				{Kind: yaml.ScalarNode, Value: "profile"}, newProfile,
			},
		},
	}}
	var buf bytes.Buffer
	enc := yaml.NewEncoder(&buf)
	enc.SetIndent(yamlIndent)
	if err := enc.Encode(outRoot); err != nil {
		return fmt.Errorf("error marshaling YAML: %v", err)
	}
	enc.Close()

	if err = os.WriteFile(dstPath, buf.Bytes(), 0o644); err != nil {
		return fmt.Errorf("error writing file %s: %v", dstPath, err)
	}

	return nil
}

func processProfileDir(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing profile directory: %s to %s", srcPath, dstPath)
	if err := os.MkdirAll(dstPath, 0o755); err != nil {
		return fmt.Errorf("error creating directory %s: %v", dstPath, err)
	}

	entries, err := os.ReadDir(srcPath)
	if err != nil {
		return fmt.Errorf("error reading directory %s: %v", srcPath, err)
	}

	for _, entry := range entries {
		srcFilePath := filepath.Join(srcPath, entry.Name())
		if entry.IsDir() {
			logger.Logger.Printf("Skipping directory: %s", srcFilePath)
			continue
		}
		if strings.HasPrefix(entry.Name(), "deployment_") || strings.HasPrefix(entry.Name(), "workspace_template") {
			dstFilePath := filepath.Join(dstPath, entry.Name())
			if err := processProfileFile(srcFilePath, dstFilePath, dataPlane); err != nil {
				return err
			}
		} else {
			logger.Logger.Printf("Skipping file: %s", srcFilePath)
		}

	}

	logger.Logger.Printf("Processed profile directory: %s to %s", srcPath, dstPath)

	return nil
}
