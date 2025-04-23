package unmesh

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/ascend-io/ascend-community-internal/oeutils/internal/logger"
)

func processFlowYamlFile(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing flow YAML file: %s to %s", srcPath, dstPath)

	if err := copyFile(srcPath, dstPath); err != nil {
		return fmt.Errorf("error copying file %s to %s: %v", srcPath, dstPath, err)
	}

	return nil
}

func processFlowSubDir(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing flow component directory: %s to %s", srcPath, dstPath)

	// create the dstPath's directory if it doesn't exist
	if err := os.MkdirAll(dstPath, 0o755); err != nil {
		return fmt.Errorf("error creating directory %s: %v", dstPath, err)
	}

	// for each compoenent directory, copy the files to the destination
	entries, err := os.ReadDir(srcPath)
	if err != nil {
		return fmt.Errorf("error reading directory %s: %v", srcPath, err)
	}

	for _, entry := range entries {
		srcFilePath := filepath.Join(srcPath, entry.Name())
		dstFilePath := filepath.Join(dstPath, entry.Name())
		if entry.IsDir() {
			if err := processFlowSubDir(srcFilePath, dstFilePath, dataPlane); err != nil {
				return err
			}
		} else {
			// process the file
			if err := processFlowComponentFile(srcFilePath, dstFilePath, dataPlane); err != nil {
				return err
			}
		}
	}

	return nil
}

func processFlowComponentFile(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing flow component file: %s to %s", srcPath, dstPath)

	data, err := os.ReadFile(srcPath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %v", srcPath, err)
	}

	modifiedData := findReplaceDataPlaneFlowRef(string(data), dataPlane)
	err = os.WriteFile(dstPath, []byte(modifiedData), 0o644)
	if err != nil {
		return fmt.Errorf("error writing file %s: %v", dstPath, err)
	}

	return nil
}

func processFlowDir(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing flow directory: %s to %s", srcPath, dstPath)

	if err := os.MkdirAll(dstPath, 0o755); err != nil {
		return fmt.Errorf("error creating directory %s: %v", dstPath, err)
	}

	entries, err := os.ReadDir(srcPath)
	if err != nil {
		return fmt.Errorf("error reading directory %s: %v", srcPath, err)
	}

	for _, entry := range entries {
		srcFilePath := filepath.Join(srcPath, entry.Name())
		dstFilePath := filepath.Join(dstPath, entry.Name())

		if entry.IsDir() {
			if err := processFlowSubDir(srcFilePath, dstFilePath, dataPlane); err != nil {
				return err
			}
		} else {
			// check if it's the flow yaml file
			if strings.HasSuffix(entry.Name(), ".yaml") {
				dstFilePath = strings.ReplaceAll(dstFilePath, "-"+dataPlane, "")
				if err := processFlowYamlFile(srcFilePath, dstFilePath, dataPlane); err != nil {
					return err
				}
			} else {
				if err := processFlowComponentFile(srcFilePath, dstFilePath, dataPlane); err != nil {
					return err
				}
			}
		}
	}

	return nil
}

func processFlowsDir(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing flows directory: %s to %s", srcPath, dstPath)

	if err := os.MkdirAll(dstPath, 0o755); err != nil {
		return fmt.Errorf("error creating directory %s: %v", dstPath, err)
	}

	entries, err := os.ReadDir(srcPath)
	if err != nil {
		return fmt.Errorf("error reading directory %s: %v", srcPath, err)
	}

	for _, entry := range entries {
		if entry.IsDir() {
			srcDirPath := filepath.Join(srcPath, entry.Name())
			if strings.HasSuffix(srcDirPath, "-"+dataPlane) {
				dstDirPath := filepath.Join(dstPath, strings.TrimSuffix(entry.Name(), "-"+dataPlane))
				if err := processFlowDir(srcDirPath, dstDirPath, dataPlane); err != nil {
					return err
				}
			} else {
				logger.Logger.Printf("Skipping directory: %s", srcDirPath)
				continue
			}
		} else {
			logger.Logger.Printf("Skipping file: %s", entry.Name())
			continue
		}
	}

	return nil
}
