package unmesh

// Central location for configuration constants and variables shared across the
// unmesh package.  Keeping these in a dedicated file avoids circular
// dependencies and makes it obvious what can be tuned by maintainers.

// Raw files copied verbatim (unless a custom strategy exists).
var rawCopyFiles = []string{
	"LICENSE",
	".gitignore",
	"ascend_project.yaml",
}

// Directory trees copied verbatim.
var rawCopyDirs = []string{
	"macros",
	"src",
	"data",
}

// Directory trees that require processing.
var editCopyDirs = []string{
	"automations",
	"connections",
	"flows",
	"profiles",
}

// Secret‑manager locations that must be anonymised in generated projects.
// Only the Google Secret Manager reference is still required.
var vaultNames = []string{
	"google_secret_manager",
}

// Display names for each data plane.
var dataPlaneMap = map[string]string{
	"bigquery":   "BigQuery",
	"databricks": "Databricks",
	"snowflake":  "Snowflake",
}
