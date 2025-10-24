# Excel Bench Seating Report Implementation

## Overview
The project has been updated to generate **Excel reports** instead of PDF reports, with a **bench seating arrangement** where 2 students sit per bench (left and right seats).

## Changes Made

### 1. Backend Changes

#### New File: `backend/services/excel_service.py`
- **Purpose**: Generates Excel reports with bench seating layout
- **Key Features**:
  - Uses `openpyxl` library for Excel file creation
  - Creates multiple sheets: Summary + one sheet per room
  - **Bench Layout**: Each row represents one bench with 2 seats (left and right)
  - **Columns**:
    - Bench #
    - Left Seat # (with gray background)
    - Left Student Name
    - Left Roll Number
    - Right Seat # (with light gray background)
    - Right Student Name
    - Right Roll Number
  - **Color Coding**:
    - Headers: Dark blue background with white text
    - Left seats: Gray background (#E7E6E6)
    - Right seats: Light gray background (#F2F2F2)
    - Borders around all cells for clarity

#### Updated: `backend/routes/allocations.py`
- Replaced `PDFService` import with `ExcelService`
- Changed file extensions from `.pdf` to `.xlsx`
- Updated MIME type to `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- All three report endpoints now generate Excel:
  1. `/allocations/<id>/report` - Full allocation report
  2. `/allocations/<id>/class-report/<year>` - Class-specific report
  3. Multi-exam reports (if applicable)

#### Updated: `backend/requirements.txt`
- Added `openpyxl==3.1.2` for Excel file generation

### 2. Frontend Changes

#### Updated: `src/services/api.js`
- Added handler for Excel MIME type (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`)
- Auto-downloads Excel files with proper filename extraction

#### Updated: `src/ExamSeatAllocator.jsx`
- Changed all "PDF" references to "Excel" in:
  - Button text: "Download Excel Report"
  - Success messages: "Excel report downloaded successfully"
  - Error messages: "Failed to generate Excel report"
  - Class report descriptions

## How Bench Seating Works

### Example Layout in Excel:

| Bench # | Left Seat # | Left Student    | Left Roll # | Right Seat # | Right Student   | Right Roll # |
|---------|-------------|-----------------|-------------|--------------|-----------------|--------------|
| 1       | 1           | John Doe        | CS001       | 2            | Jane Smith      | CS002        |
| 2       | 3           | Bob Johnson     | IT001       | 4            | Alice Brown     | IT002        |
| 3       | 5           | Charlie Davis   | CS003       | 6            | Diana Prince    | CS004        |

### Features:
1. **Bench Number**: Sequential numbering (1, 2, 3, ...)
2. **Seat Numbers**: Actual seat assignments from allocation
3. **Visual Distinction**: Different background colors for left (darker gray) and right (lighter gray) seats
4. **Odd Number Handling**: If total students is odd, last bench has only left seat filled

## Report Types Generated

### 1. Full Allocation Report
- **Filename**: `allocation_report_{id}.xlsx`
- **Sheets**:
  - Summary: Overall statistics and allocation info
  - One sheet per room with bench seating layout

### 2. Class-Specific Report
- **Filename**: `class_{year}_allocation_report_{id}.xlsx`
- **Sheets**:
  - Summary: Class-specific statistics
  - One sheet per room showing only students from that class year
  - Bench seating arrangement

### 3. Multi-Exam Report (if applicable)
- **Filename**: `multi_exam_allocation_report_{id}.xlsx`
- **Extra Columns**: Includes exam name/subject for each student

## Installation

The required package has been installed:
```bash
pip install openpyxl==3.1.2
```

## API Endpoints (Unchanged)

All endpoints remain the same, only the output format changed:
- `GET /api/allocations/<id>/report` - Returns Excel file
- `GET /api/allocations/<id>/class-report/<year>` - Returns Excel file

## Benefits of Excel Format

1. **Editable**: Users can modify reports if needed
2. **Sortable/Filterable**: Excel's built-in features
3. **Formulas**: Can add calculations if needed
4. **Professional**: Clean, formatted appearance
5. **Accessible**: Opens in Excel, Google Sheets, LibreOffice
6. **Bench Layout**: Clear visual representation of seating pairs

## Visual Design

### Summary Sheet
- Title in large, bold blue font
- Organized sections with labeled fields
- Statistics table with alternating colors

### Room Sheets
- Room name as header
- Capacity and allocation info
- Subject distribution summary
- **Bench seating table** with:
  - Bold headers (dark blue background)
  - Gray/light gray alternating for left/right seats
  - Borders for all cells
  - Auto-sized columns for readability

## Usage

1. Allocate seats using the UI
2. Click "Download Excel Report" button
3. Excel file downloads automatically
4. Open in Excel/Google Sheets/LibreOffice
5. Each room sheet shows bench seating arrangement
6. Print or share as needed

## Notes

- Original PDF service (`pdf_service.py`) is preserved but no longer used
- Can switch back to PDF by reverting import changes in `allocations.py`
- Excel files are typically larger than PDFs but more versatile
- Bench numbering starts at 1 and increments sequentially
- Seat numbers are the actual allocated seat numbers from the system
