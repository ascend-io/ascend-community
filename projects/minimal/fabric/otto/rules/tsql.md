---
otto:
  rule:
    alwaysApply: true
    description: Fabric uses the T-SQL dialect with single-connection query constraints.
---

# T-SQL dialect

This Project uses Microsoft Fabric as its data plane. Fabric uses the T-SQL dialect, **not** standard SQL (PostgreSQL, MySQL, etc.).

## Common T-SQL vs standard SQL differences

| Standard SQL | T-SQL (Fabric) |
|---|---|
| `SELECT * FROM t LIMIT 10` | `SELECT TOP 10 * FROM t` |
| `LIMIT 10 OFFSET 20` | `ORDER BY col OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` |
| `column_name AS "alias"` | `column_name AS [alias]` |
| Double-quoted identifiers `"col"` | Square-bracketed identifiers `[col]` |
| `IFNULL(a, b)` or `COALESCE(a, b)` | `ISNULL(a, b)` or `COALESCE(a, b)` |
| `CAST(x AS TEXT)` | `CAST(x AS NVARCHAR(MAX))` |
| `NOW()` or `CURRENT_TIMESTAMP` | `GETDATE()` or `CURRENT_TIMESTAMP` |
| `EXTRACT(YEAR FROM dt)` | `YEAR(dt)` or `DATEPART(YEAR, dt)` |
| `string \|\| string` | `CONCAT(string, string)` or `string + string` |
| `TRUE` / `FALSE` | `1` / `0` |
| `IF(cond, a, b)` | `IIF(cond, a, b)` or `CASE WHEN cond THEN a ELSE b END` |
| `CREATE TABLE IF NOT EXISTS` | Use `IF OBJECT_ID('t', 'U') IS NULL` guard |
| `TRUNCATE TABLE t RESTART IDENTITY` | `TRUNCATE TABLE t` (no identity restart option) |
| `AUTO_INCREMENT` | `IDENTITY(1,1)` |
| `GROUP BY 1, 2` (ordinal) | `GROUP BY col_name1, col_name2` (explicit column names required) |

## Fabric connection constraints

Fabric's ODBC driver allows only **one active result set per connection at a time**. Issuing a new query while results from a previous query are still being consumed produces:

```
('HY000', '[HY000] [Microsoft][ODBC Driver 18 for SQL Server]Connection is busy with results for another command (0) (SQLExecDirectW)')
```

### Applications

When building Applications that call `window.ascend.runQuery()`:

- **NEVER** fire multiple `runQuery()` calls in parallel (e.g. with `Promise.all`)
- **ALWAYS** `await` each `runQuery()` call sequentially before starting the next one
- If you need data from multiple queries, chain them with sequential `await` calls
- **ALWAYS** include a **Refresh button** in the top header/toolbar of every Fabric Application (see below)

#### Sequential query pattern

```javascript
// WRONG — causes "Connection is busy" on Fabric
const [a, b, c] = await Promise.all([
  window.ascend.runQuery(query1, { connection }),
  window.ascend.runQuery(query2, { connection }),
  window.ascend.runQuery(query3, { connection }),
]);

// CORRECT — sequential queries respect Fabric's single-result-set constraint
const a = await window.ascend.runQuery(query1, { connection });
const b = await window.ascend.runQuery(query2, { connection });
const c = await window.ascend.runQuery(query3, { connection });
```

#### Mandatory Refresh button

Every Fabric Application **must** include a Refresh button that is rendered unconditionally in the top-level layout — outside of any loading, error, or data-dependent branch. This ensures the user can always retry data fetching even when a query fails due to a busy connection or transient error.

Requirements:
- Render the button **before** any conditional `if (loading)` / `if (error)` return
- Place it in a persistent header/toolbar that is **always visible**
- On click, re-run the data-fetching function (reset error state, set loading, re-fetch sequentially)
- The button must never be gated behind loaded data or a successful state

```jsx
// CORRECT — Refresh button always renders regardless of loading/error state
export default function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [data, setData] = useState(null);

  const loadData = useCallback(async () => {
    setError('');
    setLoading(true);
    try {
      const a = await window.ascend.runQuery(query1, { connection });
      const b = await window.ascend.runQuery(query2, { connection });
      setData({ a: a.rows, b: b.rows });
    } catch (err) {
      setError(err?.message || 'Failed to load data.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadData(); }, [loadData]);

  // Header with Refresh ALWAYS renders — never inside a conditional branch
  return (
    <div>
      <header>
        <h1>Dashboard</h1>
        <button onClick={loadData} disabled={loading}>
          {loading ? 'Loading…' : 'Refresh'}
        </button>
      </header>
      {error && <div className="error">{error}</div>}
      {loading && <div>Loading…</div>}
      {data && <Charts data={data} />}
    </div>
  );
}
```

### SQL Components

In SQL Transforms and Tasks, each Component runs a single query, so this constraint does not typically apply. However, avoid patterns that open multiple result sets in a single statement (e.g. nested `EXEC` calls that return results).
