package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

// rootCmd is the main cobra command executed by this binary. It is intentionally
// kept very small: all real functionality lives in sub‑commands (see the `cmd`
// package). Keeping `rootCmd` minimal makes it easy to understand the CLI entry
// point at a glance and avoids accidental coupling between unrelated commands.
var rootCmd = &cobra.Command{
	Use:   "oeutils",
	Short: "Internal utils for Otto's Expeditions.",
}

func init() {}

// Execute is the program's primary entry‑point and should be invoked from
// `main.main()`. It delegates all logic to the cobra command hierarchy and
// returns only on fatal error, at which point the process is terminated with a
// non‑zero exit code. This thin wrapper exists solely so that other packages
// (e.g. tests) can programmatically execute the CLI without importing the cobra
// internals used here.
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
