---
otto:
  rule:
    alwaysApply: false
    description: |
      Guidelines for migrating ETL logic from other platforms (Informatica, SSIS, Alteryx, Trifacta, dbt, custom scripts, etc.) to Ascend;
      fetch these rules before performing any migrations.
    keywords:
      - migrate
      - migration
      - convert
---

# ETL Migration Guidelines

When migrating ETL logic from other platforms (Informatica, SSIS, Alteryx, Trifacta, dbt, custom scripts, etc.) to Ascend, follow these principles.

## Core Principle: Validate Before You Build

A migration is **not complete** until 100% of records are verified to match between the legacy system and Ascend. Build validation into every step, not as an afterthought.

---

## Migration Workflow

### 1. Understand the Source

Before writing any code:
- Review the source ETL logic (recipes, SQL, transformations, mappings)
- Identify input data sources and their schemas
- Identify expected output format and schema
- Note any platform-specific functions that need translation
- If simplified documentation exists (DAG diagrams, readable transformation specs), use it as your primary reference

### 2. Set Up Infrastructure

Create the flow structure and load data:
1. Create the flow directory with a README to track progress
2. Create read components for source data
3. Create read components for expected output (if available for validation)
4. **Do NOT create transform components yet** — validate with ad-hoc queries first

### 3. Understand Schemas First

Before creating any components, use ad-hoc queries to understand both source and expected schemas:

```sql
-- Understand expected output schema and types
DESCRIBE SELECT * FROM expected_output_table

-- Understand source data schema
DESCRIBE SELECT * FROM source_table

-- Sample expected data to understand formats
SELECT * FROM expected_output_table LIMIT 5
```

### 4. Build and Validate Transforms Iteratively

Build the complete transform based on the source logic:

```sql
-- Translate the source logic into SQL
SELECT
    UPPER(name) AS Name,
    amount * 1.1 AS AdjustedAmount,
    DATE(timestamp) AS DateField
FROM {{ ref('source_data') }} a
LEFT JOIN {{ ref('lookup_data') }} b ON a.id = b.id
WHERE status = 'active'
```

### 5. Validate with EXCEPT Pattern

The EXCEPT pattern is the most effective way to detect differences between expected and actual output:

```sql
SELECT 'expected_only' AS source, * FROM (
    SELECT * FROM expected_table
    EXCEPT DISTINCT
    SELECT * FROM actual_table
)
UNION ALL
SELECT 'actual_only' AS source, * FROM (
    SELECT * FROM actual_table
    EXCEPT DISTINCT
    SELECT * FROM expected_table
)
```

**Interpreting Results:**

| Result Pattern | Likely Cause | Action |
|----------------|--------------|--------|
| All rows in both sides | Systematic issue (types, column order, formats) | Compare schemas, check date formats |
| Some rows differ | Data-level differences | Compare specific columns for differing rows |
| expected_only has rows | Missing records in actual | Check filter criteria |
| actual_only has rows | Extra records in actual | Check filter criteria |
| Empty result | Perfect match! | ✅ Done |

**Zero rows = ✅ validated.**

### 6. Debug Column-by-Column (Only If Validation Fails)

If EXCEPT shows differences, narrow down which columns are causing the mismatch:

```sql
-- Test with subset of columns to isolate the issue
SELECT 'expected_only' AS source, * FROM (
    SELECT id, Name, Amount FROM expected_table
    EXCEPT DISTINCT
    SELECT id, Name, Amount FROM actual_table
)
UNION ALL
SELECT 'actual_only' AS source, * FROM (
    SELECT id, Name, Amount FROM actual_table
    EXCEPT DISTINCT
    SELECT id, Name, Amount FROM expected_table
)
```

Progressively remove columns until you identify which specific column(s) cause the mismatch.

### 7. Create Components Only When Validated

Once ad-hoc queries show zero differences:
1. Create the transform component with the validated SQL
2. Create comparison components for ongoing validation (optional)
3. Update the flow README with completion status

---

## Validation Methods

### Primary: EXCEPT DISTINCT

Use when both tables are accessible from the same connection. Returns 0 rows if datasets are identical.

### Fallback: Dataset Hash

When legacy and Ascend tables can't be queried from the same connection:

```sql
-- Run separately against each system
SELECT
  COUNT(*) as row_count,
  FARM_FINGERPRINT(STRING_AGG(TO_JSON_STRING(t), '' ORDER BY TO_JSON_STRING(t))) as dataset_hash
FROM <table> t
```

**Matching row_count AND dataset_hash = ✅ validated.**

### What is NOT Acceptable Validation

These do NOT constitute validation:
- ❌ Aggregate statistics (row counts, distinct values, min/max)
- ❌ Sample records (even thousands)
- ❌ Schema comparison only
- ❌ "Looks good" spot checks

---

## Progress Tracking

Track migration progress in the flow's README file:

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete and validated (EXCEPT returned 0 rows) |
| 🔄 | In progress |
| ❌ | Not started |
| ⏳ | Runs but validation not yet performed |
| ⚠️ | Blocked (document reason) |

---

## Debugging Upstream Issues

When differences can't be explained by transformation logic, traverse upstream:

### Verify Records Exist in Read Component

```sql
-- Check if expected records exist in source
SELECT * 
FROM {{ ref('read_source_data') }}
WHERE id = '12345'  -- ID from expected output
```

If records are missing from the read component, the issue is **data ingestion**, not transformation.

### Search the Raw Source File

Use file search to verify the raw source file contains the expected data. If found in source file but not in read component, check parser configuration.

---

## Common Migration Challenges

### Source Logic vs Expected Output Conflicts

**Problem:** The source transformation logic doesn't match what's in the expected output file.

**Resolution:**
1. **Expected output takes precedence** — it represents what was actually produced
2. Document the discrepancy in the flow README
3. Verify the expected output is correct by checking sample values
4. If in doubt, ask which is authoritative

### Source Data Version Mismatch

**Problem:** Expected outputs were generated from a different version of source data.

**Symptoms:**
- Transformation logic is correct but values differ
- Differences follow a pattern
- Missing or extra records that can't be explained by filter logic

**Resolution:**
- Document the mismatch in the README
- Verify transformation logic is correct by checking source data directly
- Consider regenerating expected outputs from current source data
- Accept that exact validation may not be possible

### Empty String vs NULL

Source data often has `""` for missing values, but expected output may have `NULL`. Use `NULLIF(column, '')` or `COALESCE(column, '')` to normalize.

### Type Inference Differences

Different platforms infer types differently (e.g., numeric strings → INT64 vs STRING). Fix with explicit casts in transforms.

### Platform-Specific Functions

Map legacy platform functions to SQL equivalents. Common translations:
- Date/time formatting functions
- String manipulation functions
- Null handling functions
- Regex patterns (test against actual data samples)

---

## Anti-Patterns

- ❌ Creating transform components before validating with ad-hoc queries
- ❌ Reading entire data files without checking size first
- ❌ Using `SELECT *` instead of explicit column lists during migration
- ❌ Spot-checking with LIMIT instead of full EXCEPT validation
- ❌ Guessing at transformations without reviewing source logic
- ❌ Not tracking progress in the flow README
- ❌ Assuming exact validation is possible when source data has evolved
- ❌ Blindly following source logic when expected output differs
- ❌ Assuming table locations without verifying legacy output configuration

---

## Checklist Before Marking Complete

- [ ] Legacy output location verified
- [ ] Ascend write component configured correctly
- [ ] Schema comparison completed
- [ ] Type mismatches fixed
- [ ] Platform-specific functions translated and tested
- [ ] Business logic verified against legacy code
- [ ] **EXCEPT DISTINCT returned 0 rows OR dataset hashes match**