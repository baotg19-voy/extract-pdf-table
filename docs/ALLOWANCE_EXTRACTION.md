# ALLOWANCE_EXTRACTION

## Overview

Allowance PDF contains a **single table** where each row is one employee, each column is a route type or allowance category.

## Extraction Process

```
PDF Input
    ↓
┌─────────────────────────────────────┐
│ Step 1: Read PDF with Stream        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Step 2: Find Employee Row (ID)      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Step 3: Get Name (Japanese)         │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Step 4: Map 37 Columns              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Step 5: Extract Values (Columns)    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Step 6: Compile JSON Record         │
└─────────────────────────────────────┘
    ↓
JSON Output
```

## Column Structure

```
Column 0
    ↓
┌────────────────────┐
│ Employee ID        │  (shain_id)
└────────────────────┘

Column 1
    ↓
┌────────────────────┐
│ Employee Name      │  (shimei)
└────────────────────┘

Columns 2-33
    ↓
┌────────────────────┐
│ Route Type Counts  │  (sagawa_b, ippan_ba, etc.)
└────────────────────┘

Column 34
    ↓
┌────────────────────┐
│ Temp Allowance     │  (rinji_teate)
└────────────────────┘

Column 35
    ↓
┌────────────────────┐
│ Total              │  (gokei)
└────────────────────┘
```

## Data Structure

```json
{
  "shain_id": "160013",
  "shimei": "江頭 孝之",
  "sagawa_b": 0,
  "sagawa_ba": 0,
  "sagawa_bb": 10,
  "ippan_b": 0,
  "ippan_ba": 3,
  "ippan_bb": 2,
  "rinji_teate": 3000,
  "gokei": 28
}
```

## Differences from Attendance

| Aspect | Allowance | Attendance |
|--------|-----------|-----------|
| Structure | Single table | Vertical blocks |
| Rows per employee | 1 row | 40+ rows |
| Parsing method | Stream | Lattice |
| Extraction | Direct column mapping | Field label search |

## Output

```
┌─────────────────────────────┐
│ allowance_records.json      │  Machine readable
├─────────────────────────────┤
│ allowance_records.csv       │  Spreadsheet format
├─────────────────────────────┤
│ allowance_records.md        │  Markdown table
└─────────────────────────────┘
         All: 32 records
```
