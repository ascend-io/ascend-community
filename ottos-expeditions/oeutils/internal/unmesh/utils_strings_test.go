package unmesh

import "testing"

func TestFindReplaceDataPlane(t *testing.T) {
	cases := []struct {
		in        string
		dataPlane string
		want      string
	}{
		{"my-flow-bigquery", "bigquery", "my-flow"},
		{"nochange", "bigquery", "nochange"},
		{"transform-snowflake", "snowflake", "transform"},
		{"foo-big-query", "big-query", "foo"},
	}

	for _, c := range cases {
		got := findReplaceDataPlane(c.in, c.dataPlane)
		if got != c.want {
			t.Errorf("findReplaceDataPlane(%q)=%q want %q", c.in, got, c.want)
		}
	}
}

func TestReplaceReadmeTemplates(t *testing.T) {
	in := "This project targets the {{ .DataPlane }}. Each {{ .DataPlaneLower }} has docs.\n\n## Internal\nSecret stuff"
	want := "This project targets the BigQuery. Each bigquery has docs.\n\n"
	got := replaceReadmeTemplates(in, "bigquery")
	if got != want {
		t.Errorf("replaceReadmeTemplates()=%q want %q", got, want)
	}
}

func TestFindReplaceVaultNames(t *testing.T) {
	in := "google_secret_manager foo"
	want := "environment foo"
	if got := findReplaceVaultNames(in); got != want {
		t.Errorf("findReplaceVaultNames()=%q want %q", got, want)
	}
}
