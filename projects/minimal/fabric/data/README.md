# Local Data

Local data files checked into Git for testing and development.

## Files

| File | Description |
|------|-------------|
| `goats.csv` | Sample goat data for expedition pack animals |
| `route_closures.csv` | Route closure information for expedition planning |

## Usage

These files are accessed via #connection:read_local_files and used in extract-load flows.

> [!NOTE]
> Keep local data files small. For larger datasets, use cloud storage connections.