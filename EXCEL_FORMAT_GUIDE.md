# Excel Bench Seating Format - Visual Guide

## How the Excel Output Looks

### Summary Sheet
```
┌────────────────────────────────────────────────────┐
│        Exam Seat Allocation Report                 │
├────────────────────────────────────────────────────┤
│ Generated On:     2025-10-23 15:30:00              │
│ Strategy:         Mixed                            │
│ Subject Filter:   All Subjects                     │
│                                                    │
│ Allocation Summary                                 │
│ ┌──────────────────────┬──────────────┐           │
│ │ Total Students:      │ 100          │           │
│ │ Students Allocated:  │ 95           │           │
│ │ Students Unallocated:│ 5            │           │
│ │ Rooms Used:          │ 3            │           │
│ │ Allocation Rate:     │ 95%          │           │
│ │ Quality Rating:      │ Excellent    │           │
│ └──────────────────────┴──────────────┘           │
└────────────────────────────────────────────────────┘
```

### Room Sheet Example (Lab-1)
```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            Room: Lab-1                                                         │
│                    Capacity: 30 | Allocated: 25 | Benches: 13                                 │
│                    Subject Distribution: CS101: 15 | IT201: 10                                │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Bench # │ Left Seat # │ Left Student    │ Left Roll # │ Right Seat # │ Right Student  │ Right Roll # │
├─────────┼─────────────┼─────────────────┼─────────────┼──────────────┼────────────────┼──────────────┤
│    1    │      1      │ John Doe        │   CS001     │      2       │ Jane Smith     │    CS002     │
│         │   (gray)    │    (gray)       │   (gray)    │  (lt-gray)   │  (lt-gray)     │  (lt-gray)   │
├─────────┼─────────────┼─────────────────┼─────────────┼──────────────┼────────────────┼──────────────┤
│    2    │      3      │ Bob Johnson     │   IT001     │      4       │ Alice Brown    │    IT002     │
│         │   (gray)    │    (gray)       │   (gray)    │  (lt-gray)   │  (lt-gray)     │  (lt-gray)   │
├─────────┼─────────────┼─────────────────┼─────────────┼──────────────┼────────────────┼──────────────┤
│    3    │      5      │ Charlie Davis   │   CS003     │      6       │ Diana Prince   │    CS004     │
│         │   (gray)    │    (gray)       │   (gray)    │  (lt-gray)   │  (lt-gray)     │  (lt-gray)   │
├─────────┼─────────────┼─────────────────┼─────────────┼──────────────┼────────────────┼──────────────┤
│   ...   │     ...     │      ...        │     ...     │     ...      │      ...       │     ...      │
├─────────┼─────────────┼─────────────────┼─────────────┼──────────────┼────────────────┼──────────────┤
│   13    │     25      │ Eve Adams       │   IT003     │              │                │              │
│         │   (gray)    │    (gray)       │   (gray)    │  (lt-gray)   │  (lt-gray)     │  (lt-gray)   │
└─────────┴─────────────┴─────────────────┴─────────────┴──────────────┴────────────────┴──────────────┘
```

## Color Scheme

### Headers (Row 5)
- **Background**: Dark Blue (#1F4E78)
- **Text**: White
- **Font**: Bold, Size 11

### Left Seat Columns (Columns B, C, D)
- **Background**: Gray (#E7E6E6)
- **Border**: Thin black border on all sides
- **Seat Number**: Bold font

### Right Seat Columns (Columns E, F, G)
- **Background**: Light Gray (#F2F2F2)
- **Border**: Thin black border on all sides
- **Seat Number**: Bold font

### Bench Number (Column A)
- **Font**: Bold
- **Alignment**: Center

## Bench Seating Logic

### Normal Case (Even Students)
```
Students: [S1, S2, S3, S4, S5, S6]
Benches:
  Bench 1: S1 (Seat 1) | S2 (Seat 2)
  Bench 2: S3 (Seat 3) | S4 (Seat 4)
  Bench 3: S5 (Seat 5) | S6 (Seat 6)
```

### Odd Students Case
```
Students: [S1, S2, S3, S4, S5]
Benches:
  Bench 1: S1 (Seat 1) | S2 (Seat 2)
  Bench 2: S3 (Seat 3) | S4 (Seat 4)
  Bench 3: S5 (Seat 5) | (empty)
```

## Excel Features

### Cell Formatting
- All cells have borders for clear separation
- Column widths auto-adjusted for readability
- Text alignment:
  - Bench numbers: Center
  - Seat numbers: Center
  - Names: Left
  - Roll numbers: Center

### Sheets Organization
1. **Summary** - Overview and statistics
2. **Room 1** - First room's bench layout
3. **Room 2** - Second room's bench layout
4. **Room N** - Additional rooms...

### Professional Appearance
- Clean, grid-like structure
- Easy to read and print
- Suitable for distribution to exam supervisors
- Can be printed and posted outside exam rooms

## Use Cases

### For Exam Supervisors
- Print room sheets and post outside exam halls
- Clear bench and seat numbering
- Easy to verify student positions

### For Administration
- Summary sheet shows overall statistics
- Can verify allocation quality
- Track room utilization

### For Students
- Class-specific reports show only their classmates
- Easy to find their seat and bench number
- Know who sits next to them (bench partner)

## Export and Print

### Recommended Print Settings
- **Orientation**: Landscape
- **Fit to**: 1 page wide
- **Margins**: Narrow
- **Gridlines**: Print (optional, borders already included)

### File Sharing
- Email as attachment (smaller than PDF)
- Upload to Google Drive/OneDrive
- Open in Google Sheets for cloud access
- Convert to PDF if needed (Print → Save as PDF)
