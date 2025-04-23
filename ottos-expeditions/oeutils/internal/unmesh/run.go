package unmesh

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/ascend-io/ascend-community-internal/oeutils/internal/logger"
)

// NOTE: The following configuration values were previously spread across the
// codebase as un‑documented global variables.  Centralising them here makes it
// obvious which parts of the codebase are configuration knobs versus business
// logic and avoids the accidental introduction of additional globals in the
// future.
// editDirProcessors maps directory names to their specialised processing
// functions. This declarative approach makes it straightforward to add new
// directory types without modifying the control‑flow logic in processEditDirs.
var editDirProcessors = map[string]func(srcPath, dstPath, dataPlane string) error{
	"automations": processAutomationDir,
	"connections": processConnectionsDir,
	"flows":       processFlowsDir,
	"profiles":    processProfileDir,
}

func processEditDirs(sourceDir, destDir, dataPlane string) error {
	for _, dir := range editCopyDirs {
		srcPath := filepath.Join(sourceDir, dir)
		dstPath := filepath.Join(destDir, dir)

		if _, err := os.Stat(srcPath); os.IsNotExist(err) {
			logger.Logger.Printf("Warning: Source directory does not exist: %s", srcPath)
			continue
		}

		processor, ok := editDirProcessors[dir]
		if !ok {
			logger.Logger.Printf("Warning: Unknown directory type: %s", dir)
			continue
		}

		if err := processor(srcPath, dstPath, dataPlane); err != nil {
			return err
		}
	}

	return nil
}

func unmeshProject(meshProjectDir string, dataPlane string) error {
	projectsDir := filepath.Dir(meshProjectDir)
	dataPlaneDir := filepath.Join(projectsDir, dataPlane)

	if err := removeDirectory(dataPlaneDir); err != nil {
		return fmt.Errorf("error removing directory %s: %w", dataPlaneDir, err)
	}

	if err := createDirectory(dataPlaneDir); err != nil {
		return fmt.Errorf("error creating directory %s: %w", dataPlaneDir, err)
	}

	if err := copyRawFiles(meshProjectDir, dataPlaneDir, dataPlane); err != nil {
		return fmt.Errorf("error copying raw files: %w", err)
	}

	if err := copyRawDirs(meshProjectDir, dataPlaneDir); err != nil {
		return fmt.Errorf("error copying raw directories: %w", err)
	}

	if err := processEditDirs(meshProjectDir, dataPlaneDir, dataPlane); err != nil {
		return fmt.Errorf("error processing directories with flow references: %w", err)
	}

	logger.Logger.Printf("successfully unmeshed for data plane: %s", dataPlane)
	return nil
}

// RunUnmesh is the public entry‑point executed by the `oeutils unmesh` command.
// It turns the monolithic `mesh` Ascend project into one project per supported
// data plane by performing the following high‑level steps:
//  1. Locates the `projects/mesh` directory relative to the current working
//     directory (so the CLI can be run from anywhere inside the repository).
//  2. For each supported data plane (see `dataPlaneMap`) it creates a sibling
//     directory named after the data plane, copying files/directories either
//     verbatim or with data‑plane specific transformations applied.
//  3. Logs progress and terminates the process with a fatal error if any step
//     fails. Using a fatal logger here is acceptable because this function is
//     only called from the CLI path where abrupt termination is the expected
//     behaviour.
//
// The heavy lifting is delegated to `unmeshProject`, keeping this function
// short and easy to read.
func RunUnmesh() {
	logger.Logger.Println("unmesh called")
	defer logger.Logger.Println("unmesh completed")

	// The CLI can be invoked from any sub‑directory in the repository.
	// Normalising the working directory here allows us to reliably locate
	// `projects/mesh` regardless of where the command was executed from.
	cwd, err := os.Getwd()
	if err != nil {
		logger.Logger.Fatalf("unable to determine working directory: %v", err)
	}

	meshProjectDir := filepath.Join(filepath.Dir(cwd), "projects", "mesh")
	logger.Logger.Printf("mesh project directory: %s", meshProjectDir)

	if _, err := os.Stat(meshProjectDir); os.IsNotExist(err) {
		logger.Logger.Fatalf("mesh project directory does not exist: %s", meshProjectDir)
	}

	for dataPlane := range dataPlaneMap {
		logger.Logger.Printf("unmeshing for data plane: %s", dataPlane)
		if err := unmeshProject(meshProjectDir, dataPlane); err != nil {
			logger.Logger.Fatalf("error unmeshing for data plane %s: %v", dataPlane, err)
		}
	}
}
