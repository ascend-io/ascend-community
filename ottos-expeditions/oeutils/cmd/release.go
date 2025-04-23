package cmd

import (
	"github.com/ascend-io/ascend-community-internal/oeutils/internal/release"
	"github.com/spf13/cobra"
)

var (
	yesFlag bool
)

// releaseCmd implements the `oeutils release` sub‑command which synchronises
// the (already un‑meshed) Ascend projects to the public ascend‑community
// repository.  Use the `--yes/-y` flag to automatically push the commit
// instead of leaving it staged in the temporary clone for manual inspection.
var releaseCmd = &cobra.Command{
	Use:   "release",
	Short: "Sync unmeshed code to the public ascend-community repository",
	Run: func(cmd *cobra.Command, args []string) {
		release.RunRelease(yesFlag)
	},
}

func init() {
	rootCmd.AddCommand(releaseCmd)

	releaseCmd.Flags().BoolVarP(&yesFlag, "yes", "y", false, "Automatically push the sync commit to origin after committing")
}
