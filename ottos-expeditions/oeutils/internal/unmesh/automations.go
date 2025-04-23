package unmesh

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"

	"github.com/ascend-io/ascend-community-internal/oeutils/internal/logger"
)

func processAutomationFile(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing automation file: %s to %s", srcPath, dstPath)

	data, err := os.ReadFile(srcPath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %v", srcPath, err)
	}
	modifiedData := findReplaceDataPlane(string(data), dataPlane)
	return os.WriteFile(dstPath, []byte(modifiedData), 0o644)
}

func processAutomationDir(srcPath string, dstPath string, dataPlane string) error {
	logger.Logger.Printf("Processing automation directory: %s to %s", srcPath, dstPath)

	if err := os.MkdirAll(dstPath, 0o755); err != nil {
		return fmt.Errorf("error creating directory %s: %v", dstPath, err)
	}

	entries, err := os.ReadDir(srcPath)
	if err != nil {
		return fmt.Errorf("error reading directory %s: %v", srcPath, err)
	}

	for _, entry := range entries {
		if !regexp.MustCompile(fmt.Sprintf(`-%s`, regexp.QuoteMeta(dataPlane))).MatchString(entry.Name()) {
			logger.Logger.Printf("Skipping file: %s", entry.Name())
			continue
		}

		srcFilePath := filepath.Join(srcPath, entry.Name())
		dstFilePath := filepath.Join(dstPath, findReplaceDataPlane(entry.Name(), dataPlane))

		if entry.IsDir() {
			if err := processAutomationDir(srcFilePath, dstFilePath, dataPlane); err != nil {
				return err
			}
		} else {
			if err := processAutomationFile(srcFilePath, dstFilePath, dataPlane); err != nil {
				return err
			}
		}
	}

	return nil
}
