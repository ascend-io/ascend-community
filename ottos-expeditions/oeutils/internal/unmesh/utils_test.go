package unmesh

import (
	"fmt"
	"strings"
	"testing"
)

// prettyDiff returns a formatted string highlighting differences between expected and actual strings
func prettyDiff(expected, actual string) string {
	if expected == actual {
		return "No differences"
	}

	expectedLines := strings.Split(expected, "\n")
	actualLines := strings.Split(actual, "\n")

	var diff strings.Builder
	diff.WriteString("\nDifferences:\n")

	// Show line-by-line differences
	maxLines := max(len(actualLines), len(expectedLines))

	for i := range maxLines {
		if i >= len(expectedLines) {
			diff.WriteString(fmt.Sprintf("Line %d: (no expected) | ACTUAL: %s\n", i+1, actualLines[i]))
		} else if i >= len(actualLines) {
			diff.WriteString(fmt.Sprintf("Line %d: EXPECTED: %s | (no actual)\n", i+1, expectedLines[i]))
		} else if expectedLines[i] != actualLines[i] {
			diff.WriteString(fmt.Sprintf("Line %d: EXPECTED: %s | ACTUAL: %s\n", i+1, expectedLines[i], actualLines[i]))
		}
	}

	return diff.String()
}

func TestFindReplaceDataPlaneFlowRef(t *testing.T) {
	tests := []struct {
		name       string
		codeString string
		dataPlane  string
		expected   string
	}{
		{
			name: "Basic Python Example",
			codeString: `@transform(
    inputs=[ref("read_sales_stores", flow="extract-load-bigquery")],
    materialized="table",
)`,
			dataPlane: "bigquery",
			expected: `@transform(
    inputs=[ref("read_sales_stores", flow="extract-load")],
    materialized="table",
)`,
		},
		{
			name:       "Basic SQL Example",
			codeString: `SELECT * FROM ${ref("other_table", flow="extract-load-bigquery")}`,
			dataPlane:  "bigquery",
			expected:   `SELECT * FROM ${ref("other_table", flow="extract-load")}`,
		},
		{
			name:       "Different Quotes",
			codeString: `inputs=[ref('read_sales_stores', flow='extract-load-bigquery')],`,
			dataPlane:  "bigquery",
			expected:   `inputs=[ref('read_sales_stores', flow='extract-load')],`,
		},
		{
			name:       "Different Whitespace",
			codeString: `inputs=[ref("read_sales_stores", flow = "extract-load-bigquery")],`,
			dataPlane:  "bigquery",
			expected:   `inputs=[ref("read_sales_stores", flow = "extract-load")],`,
		},
		{
			name:       "Extra Whitespace",
			codeString: `inputs=[ref("read_sales_stores", flow  =  "extract-load-bigquery")],`,
			dataPlane:  "bigquery",
			expected:   `inputs=[ref("read_sales_stores", flow  =  "extract-load")],`,
		},
		{
			name: "Multiple References",
			codeString: `
@transform(
    inputs=[
        ref("table1", flow="extract-load-bigquery"),
        ref("table2", flow="extract-load-bigquery")
    ],
)`,
			dataPlane: "bigquery",
			expected: `
@transform(
    inputs=[
        ref("table1", flow="extract-load"),
        ref("table2", flow="extract-load")
    ],
)`,
		},
		{
			name:       "Different Data Plane",
			codeString: `inputs=[ref("read_sales_stores", flow="extract-load-snowflake")],`,
			dataPlane:  "snowflake",
			expected:   `inputs=[ref("read_sales_stores", flow="extract-load")],`,
		},
		{
			name:       "No Match",
			codeString: `inputs=[ref("read_sales_stores", flow="extract-load-snowflake")],`,
			dataPlane:  "bigquery",
			expected:   `inputs=[ref("read_sales_stores", flow="extract-load-snowflake")],`,
		},
		{
			name: "Flow Reference Across Multiple Lines",
			codeString: `inputs=[ref("read_sales_stores", 
                flow="extract-load-bigquery")],`,
			dataPlane: "bigquery",
			expected: `inputs=[ref("read_sales_stores", 
                flow="extract-load")],`,
		},
		{
			name:       "Special Characters in Data Plane",
			codeString: `inputs=[ref("read_sales_stores", flow="extract-load-big.query")],`,
			dataPlane:  "big.query",
			expected:   `inputs=[ref("read_sales_stores", flow="extract-load")],`,
		},
		{
			name:       "Regex Special Characters in Data Plane",
			codeString: `inputs=[ref("read_sales_stores", flow="extract-load-big+query")],`,
			dataPlane:  "big+query",
			expected:   `inputs=[ref("read_sales_stores", flow="extract-load")],`,
		},
		{
			name: "Multiple Flow Prefixes",
			codeString: `
@transform(
    inputs=[
        ref("table1", flow="extract-load-bigquery"),
        ref("table2", flow="transform-bigquery"),
        ref("table3", flow="report-bigquery")
    ],
)`,
			dataPlane: "bigquery",
			expected: `
@transform(
    inputs=[
        ref("table1", flow="extract-load"),
        ref("table2", flow="transform"),
        ref("table3", flow="report")
    ],
)`,
		},
		{
			name: "Incomplete Matches",
			codeString: `
@transform(
    inputs=[
        ref("table1", flow="extract-load-bigquery"),
        ref("table2", flow="extract-load"),
        ref("table3", flow="bigquery-extract-load")
    ],
)`,
			dataPlane: "bigquery",
			expected: `
@transform(
    inputs=[
        ref("table1", flow="extract-load"),
        ref("table2", flow="extract-load"),
        ref("table3", flow="bigquery-extract-load")
    ],
)`,
		},
		{
			name:       "Empty Input",
			codeString: "",
			dataPlane:  "bigquery",
			expected:   "",
		},
		{
			name:       "Empty Data Plane",
			codeString: `inputs=[ref("read_sales_stores", flow="extract-load-")],`,
			dataPlane:  "",
			expected:   `inputs=[ref("read_sales_stores", flow="extract-load-")],`,
		},
		{
			name:       "Case Sensitivity Test",
			codeString: `inputs=[ref("read_sales_stores", flow="extract-load-BIGQUERY")],`,
			dataPlane:  "bigquery",
			expected:   `inputs=[ref("read_sales_stores", flow="extract-load-BIGQUERY")],`,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := findReplaceDataPlaneFlowRef(tt.codeString, tt.dataPlane)
			if result != tt.expected {
				t.Errorf("findReplaceDataPlaneFlowRef() failed:\n%s", prettyDiff(tt.expected, result))
			}
		})
	}
}

// TestFindReplaceDataPlaneFlowRef_RealWorldExamples tests the function with more complex real-world examples
func TestFindReplaceDataPlaneFlowRef_RealWorldExamples(t *testing.T) {
	// Python file with multiple transformations
	pythonExample := `
import ibis
import ascend_project_code.transform as T

from ascend.resources import ref, transform, test
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref("read_sales_stores", flow="extract-load-bigquery"),
        ref("read_products", flow="extract-load-bigquery")
    ],
    materialized="table",
    tests=[test("not_null", column="timestamp")],
)
def sales_stores(
    read_sales_stores: ibis.Table,
    read_products: ibis.Table,
    context: ComponentExecutionContext
) -> ibis.Table:
    sales_stores = T.clean(read_sales_stores)
    return sales_stores.join(read_products)

@transform(
    inputs=[ref("sales_stores", flow="transform-bigquery")],
    materialized="table",
)
def aggregated_sales(
    sales_stores: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    return sales_stores.aggregate()
`

	expectedPython := `
import ibis
import ascend_project_code.transform as T

from ascend.resources import ref, transform, test
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref("read_sales_stores", flow="extract-load"),
        ref("read_products", flow="extract-load")
    ],
    materialized="table",
    tests=[test("not_null", column="timestamp")],
)
def sales_stores(
    read_sales_stores: ibis.Table,
    read_products: ibis.Table,
    context: ComponentExecutionContext
) -> ibis.Table:
    sales_stores = T.clean(read_sales_stores)
    return sales_stores.join(read_products)

@transform(
    inputs=[ref("sales_stores", flow="transform")],
    materialized="table",
)
def aggregated_sales(
    sales_stores: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    return sales_stores.aggregate()
`

	// SQL file with complex formatting
	sqlExample := `
-- This is a complex SQL file with multiple references
CREATE OR REPLACE TABLE my_table AS
SELECT * 
FROM ${ref("other_table", 
        flow = "extract-load-bigquery")}
WHERE status = 'active';

-- Another reference with different formatting
INSERT INTO another_table
SELECT * FROM ${ref("source_table", flow="extract-load-bigquery")}
UNION ALL
SELECT * FROM ${ref("backup_table", flow =
    "backup-bigquery")}

-- A reference that shouldn't be changed
SELECT * FROM ${ref("unchanged_table", flow="different-pattern")}
`

	expectedSQL := `
-- This is a complex SQL file with multiple references
CREATE OR REPLACE TABLE my_table AS
SELECT * 
FROM ${ref("other_table", 
        flow = "extract-load")}
WHERE status = 'active';

-- Another reference with different formatting
INSERT INTO another_table
SELECT * FROM ${ref("source_table", flow="extract-load")}
UNION ALL
SELECT * FROM ${ref("backup_table", flow =
    "backup")}

-- A reference that shouldn't be changed
SELECT * FROM ${ref("unchanged_table", flow="different-pattern")}
`

	// Test Python example
	t.Run("Complex Python File", func(t *testing.T) {
		result := findReplaceDataPlaneFlowRef(pythonExample, "bigquery")
		if result != expectedPython {
			t.Errorf("Failed on complex Python example:%s", prettyDiff(expectedPython, result))
		}
	})

	// Test SQL example
	t.Run("Complex SQL File", func(t *testing.T) {
		result := findReplaceDataPlaneFlowRef(sqlExample, "bigquery")
		if result != expectedSQL {
			t.Errorf("Failed on complex SQL example:%s", prettyDiff(expectedSQL, result))
		}
	})
}
