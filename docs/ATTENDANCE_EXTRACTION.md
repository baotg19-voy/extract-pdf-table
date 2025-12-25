# Attendance Extraction

## Overview

Extracts employee attendance and salary data from PDF. Each table contains 4 employees with salary fields in column 6.

## Usage

```bash
# Extract attendance data
python app.py attendance

# Test against expected output
python app.py attendance --test
```

## PDF Structure

- **8 tables** in PDF, each with **4 employees**
- Employees at rows 2, 16, 30, 44 in each table
- **Column 6** contains all salary data
- Two data formats:
  - Standard: `'label\n...\ncount\namount'`
  - Reversed: `'...\ncount\namount\nlabel'`

## Extraction Flow

```
PDF → Camelot (lattice) → Find employees → Extract column 6 → Parse fields → JSON
```

## Output

- `output/attendance/attendance_records.json`
- `output/attendance/attendance_records.csv`
- `output/attendance/attendance_records.md`

**32 employee records** with 16 fields each.
