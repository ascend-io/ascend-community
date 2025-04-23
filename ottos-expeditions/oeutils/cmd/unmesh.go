package cmd

import (
	"github.com/ascend-io/ascend-community-internal/oeutils/internal/unmesh"
	"github.com/spf13/cobra"
)

var unmeshCmd = &cobra.Command{
	Use:   "unmesh",
	Short: "Unmesh the `mesh` project into projects for each Data Plane.",
	Run: func(cmd *cobra.Command, args []string) {
		unmesh.RunUnmesh()
	},
}

func init() {
	rootCmd.AddCommand(unmeshCmd)
}
