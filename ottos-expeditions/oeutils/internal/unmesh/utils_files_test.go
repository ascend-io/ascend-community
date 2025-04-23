package unmesh

import (
	"os"
	"path/filepath"
	"testing"
)

// TestReadmeCopyStrategy exercises the README rewrite logic on disk using a
// temporary directory. It ensures the destination file is created and the
// placeholders are replaced correctly.
func TestReadmeCopyStrategy(t *testing.T) {
	tmpDir := t.TempDir()

	src := filepath.Join(tmpDir, "README.md")
	dstDir := filepath.Join(tmpDir, "dst")
	dst := filepath.Join(dstDir, "README.md")

	const content = "{{ .DataPlane }} + {{ .DataPlaneLower }}\n\n## Internal\nshould-be-removed"

	if err := os.WriteFile(src, []byte(content), 0o644); err != nil {
		t.Fatalf("unable to write src readme: %v", err)
	}

	if err := readmeCopyStrategy(src, dst, "snowflake"); err != nil {
		t.Fatalf("readmeCopyStrategy() error = %v", err)
	}

	gotBytes, err := os.ReadFile(dst)
	if err != nil {
		t.Fatalf("unable to read dst readme: %v", err)
	}

	want := "Snowflake + snowflake\n\n"
	if string(gotBytes) != want {
		t.Errorf("unexpected transformed README: got %q want %q", string(gotBytes), want)
	}
}
