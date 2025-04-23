package unmesh

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/ascend-io/ascend-community-internal/oeutils/internal/logger"
)

func processConnectionFile(srcPath string, dstPath string) error {
	data, err := os.ReadFile(srcPath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %v", srcPath, err)
	}

	modifiedData := findReplaceVaultNames(string(data))

	err = os.WriteFile(dstPath, []byte(modifiedData), 0o644)
	if err != nil {
		return fmt.Errorf("error writing file %s: %v", dstPath, err)
	}

	return nil
}

func processConnectionsDir(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing connections directory: %s to %s", srcPath, dstPath)
	if err := os.MkdirAll(dstPath, 0o755); err != nil {
		return fmt.Errorf("error creating directory %s: %v", dstPath, err)
	}

	entries, err := os.ReadDir(srcPath)
	if err != nil {
		return fmt.Errorf("error reading directory %s: %v", srcPath, err)
	}

	dataPlanePrefix := "data_plane_"
	targetDataPlaneFile := fmt.Sprintf("%s%s.yaml", dataPlanePrefix, dataPlane)

	for _, entry := range entries {
		fileName := entry.Name()

		// Check if this is a data_plane file
		if strings.HasPrefix(fileName, dataPlanePrefix) {
			// Only process this data_plane file if it matches our target dataPlane
			if fileName == targetDataPlaneFile {
				srcFilePath := filepath.Join(srcPath, fileName)
				dstFilePath := filepath.Join(dstPath, fileName)
				if err := processConnectionFile(srcFilePath, dstFilePath); err != nil {
					return err
				}
			} else {
				logger.Logger.Printf("Skipping data plane file: %s", fileName)
			}
		} else {
			// Process all non-data_plane files
			srcFilePath := filepath.Join(srcPath, fileName)
			dstFilePath := filepath.Join(dstPath, fileName)
			if err := processConnectionFile(srcFilePath, dstFilePath); err != nil {
				return err
			}
		}
	}

	return nil
}
