package unmesh

import (
	"os"
	"path/filepath"
	"testing"

	"gopkg.in/yaml.v3"
)

// sampleInputYAML is a baseline project YAML with multiple data_planes and defaults
const sampleInputYAML = `project:
  name: test-project
  pip_packages:
    - pkg1
  parameters:
    data_planes:
      bigquery:
        param1: val1
      snowflake:
        param2: val2
      databricks:
        param3: val3
  defaults:
    - kind: Flow
      name:
        regex: ".*-bigquery"
      spec:
        data_plane:
          connection_name: data_plane_bigquery
    - kind: Flow
      name:
        regex: "job-.*-snowflake"
      spec:
        data_plane:
          connection_name: data_plane_snowflake
`

// TestProjectCopyStrategy_BigQuery verifies that projectCopyStrategy keeps only
// the BigQuery parameters and defaults, and strips the "-bigquery" suffix in regex.
func TestProjectCopyStrategy_BigQuery(t *testing.T) {
	dir := t.TempDir()
	src := filepath.Join(dir, "ascend_project.yaml")
	dst := filepath.Join(dir, "out.yaml")
	// Use sample input YAML
	input := sampleInputYAML
	if err := os.WriteFile(src, []byte(input), 0o644); err != nil {
		t.Fatalf("failed to write input YAML: %v", err)
	}
	// Execute strategy
	if err := projectCopyStrategy(src, dst, "bigquery"); err != nil {
		t.Fatalf("projectCopyStrategy error: %v", err)
	}
	outData, err := os.ReadFile(dst)
	if err != nil {
		t.Fatalf("failed to read output YAML: %v", err)
	}
	// Unmarshal to generic structure
	var out interface{}
	if err := yaml.Unmarshal(outData, &out); err != nil {
		t.Fatalf("failed to unmarshal output YAML: %v", err)
	}
	m, ok := out.(map[string]interface{})
	if !ok {
		t.Fatalf("expected map[string]interface{}, got %T", out)
	}
	// Check project section
	proj, ok := m["project"].(map[string]interface{})
	if !ok {
		t.Fatalf("expected project map, got %T", m["project"])
	}
	if name, _ := proj["name"].(string); name != "test-project" {
		t.Errorf("unexpected name: %v", name)
	}
	// pip_packages
	pkgs, ok := proj["pip_packages"].([]interface{})
	if !ok || len(pkgs) != 1 || pkgs[0] != "pkg1" {
		t.Errorf("unexpected pip_packages: %v", proj["pip_packages"])
	}
	// parameters.data_planes.bigquery exists, others removed
	params, ok := proj["parameters"].(map[string]interface{})
	if !ok {
		t.Fatalf("expected parameters map, got %T", proj["parameters"])
	}
	dps, ok := params["data_planes"].(map[string]interface{})
	if !ok {
		t.Fatalf("expected data_planes map, got %T", params["data_planes"])
	}
	if len(dps) != 1 {
		t.Errorf("expected only one data_plane, got %d", len(dps))
	}
	bq, ok := dps["bigquery"].(map[string]interface{})
	if !ok {
		t.Fatalf("expected bigquery map, got %T", dps["bigquery"])
	}
	if v, _ := bq["param1"].(string); v != "val1" {
		t.Errorf("unexpected bigquery.param1: %v", bq["param1"])
	}
	// defaults
	defs, ok := proj["defaults"].([]interface{})
	if !ok {
		t.Fatalf("expected defaults slice, got %T", proj["defaults"])
	}
	if len(defs) != 1 {
		t.Errorf("expected 1 default, got %d", len(defs))
	}
	def0, ok := defs[0].(map[string]interface{})
	if !ok {
		t.Fatalf("expected default entry map, got %T", defs[0])
	}
	// Check regex was stripped
	nameMap, _ := def0["name"].(map[string]interface{})
	if regex, _ := nameMap["regex"].(string); regex != ".*" {
		t.Errorf("expected regex '.*', got %q", regex)
	}
}

// TestProjectCopyStrategy_Snowflake verifies that projectCopyStrategy keeps only
// the Snowflake parameters and defaults, and strips the "-snowflake" suffix in regex.
func TestProjectCopyStrategy_Snowflake(t *testing.T) {
	dir := t.TempDir()
	src := filepath.Join(dir, "ascend_project.yaml")
	dst := filepath.Join(dir, "out.yaml")
	// Use sample input YAML
	input := sampleInputYAML
	if err := os.WriteFile(src, []byte(input), 0o644); err != nil {
		t.Fatalf("failed to write input YAML: %v", err)
	}
	if err := projectCopyStrategy(src, dst, "snowflake"); err != nil {
		t.Fatalf("projectCopyStrategy error: %v", err)
	}
	outData, err := os.ReadFile(dst)
	if err != nil {
		t.Fatalf("failed to read output YAML: %v", err)
	}
	var out interface{}
	if err := yaml.Unmarshal(outData, &out); err != nil {
		t.Fatalf("failed to unmarshal output YAML: %v", err)
	}
	m, ok := out.(map[string]interface{})
	if !ok {
		t.Fatalf("expected map[string]interface{}, got %T", out)
	}
	proj, ok := m["project"].(map[string]interface{})
	if !ok {
		t.Fatalf("expected project map, got %T", m["project"])
	}
	// parameters.data_planes.snowflake exists, others removed
	params, _ := proj["parameters"].(map[string]interface{})
	dps, _ := params["data_planes"].(map[string]interface{})
	if len(dps) != 1 {
		t.Errorf("expected only one data_plane, got %d", len(dps))
	}
	sf, ok := dps["snowflake"].(map[string]interface{})
	if !ok {
		t.Fatalf("expected snowflake map, got %T", dps["snowflake"])
	}
	if v, _ := sf["param2"].(string); v != "val2" {
		t.Errorf("unexpected snowflake.param2: %v", v)
	}
	// defaults
	defs, _ := proj["defaults"].([]interface{})
	if len(defs) != 1 {
		t.Errorf("expected 1 default, got %d", len(defs))
	}
	def0, _ := defs[0].(map[string]interface{})
	nameMap, _ := def0["name"].(map[string]interface{})
	if regex, _ := nameMap["regex"].(string); regex != "job-.*" {
		t.Errorf("expected regex 'job-.*', got %q", regex)
	}
	// spec.connection_name should remain correct
	spec, _ := def0["spec"].(map[string]interface{})
	dp, _ := spec["data_plane"].(map[string]interface{})
	if conn, _ := dp["connection_name"].(string); conn != "data_plane_snowflake" {
		t.Errorf("unexpected connection_name: %v", conn)
	}
}
