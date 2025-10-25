# Strict Adjacent Seating Implementation

## Overview
Enhanced the exam seat allocator with strict anti-copying rules and grid-based layout visualization. The system now prevents students with the same subject from sitting beside (on same bench) or across (same column, different row) from each other.

## Key Changes

### 1. Strict Placement Rules (STRICT_MODE)

**Location**: `backend/services/allocation_service.py`

Added new configuration:
```python
self.STRICT_MODE = True  # Enable strict no-adjacent rule
self.MAX_ATTEMPTS = 2000  # Increased for more placement attempts
```

#### Placement Rules in STRICT_MODE:
- ❌ **NO BESIDE**: Students with same subject cannot sit on the same bench (left/right)
- ❌ **NO ACROSS**: Students with same subject cannot sit in the same column (directly in front/behind)
- ✅ **ALLOW BEHIND**: Students with same subject CAN sit in different columns (diagonally behind)

### 2. Grid Calculation System

**New Method**: `_calculate_seat_grid(seat_num, capacity)`

Converts linear seat numbers into 2D grid coordinates:
```python
{
    'row': 0-N,           # Row number in the room
    'col': 0-3,           # Column number (bench position)
    'position': 'left'/'right',  # Side of bench
    'bench_num': 1-N      # Bench number (1-indexed)
}
```

**Room Layout Assumptions**:
- 2 students per bench (left and right seats)
- 4 benches per row (standard classroom layout)
- Total benches = capacity ÷ 2
- Total rows = ⌈total_benches ÷ 4⌉

**Example**: 60-seat room
- Total benches: 30
- Layout: 8 rows × 4 columns
- Seats: 1-2 (Bench 1, Row 0, Col 0), 3-4 (Bench 2, Row 0, Col 1), etc.

### 3. Enhanced Seat Validation

**Modified Method**: `_can_place_subject_at_seat()`

**STRICT_MODE Logic**:
```python
if same_subject_exists:
    if same_bench_num:
        return False  # Cannot sit beside
    if same_column:
        return False  # Cannot sit across
    # Different column = OK (behind is allowed)
```

**Standard Mode**: Falls back to MIN_DISTANCE=2 requirement

### 4. Room Layout Metadata

Each room allocation now includes:
```python
'room_layout': {
    'total_benches': 30,
    'benches_per_row': 4,
    'total_rows': 8,
    'total_columns': 4,
    'capacity': 60
}
```

Each student allocation includes:
```python
'grid': {
    'row': 2,
    'col': 1,
    'position': 'right',
    'bench_num': 10
}
```

### 5. Grid Visualization in Excel

**Location**: `backend/services/excel_service.py`

**New Method**: `_create_grid_visualization_sheet()`

Creates a visual grid representation showing:
- Row/column layout matching physical room arrangement
- Left (L) and Right (R) seat positions
- Student roll numbers with primary subjects
- Color coding: Left seats (gray), Right seats (light gray), Empty seats (darker gray)

**Excel Structure**:
```
Grid Layout - Room Name
Layout: 8 rows × 4 columns | 4 benches per row | 2 seats per bench

     Col 0    Col 1    Col 2    Col 3
      L   R    L   R    L   R    L   R
Row 0 [student data in cells]
Row 1 [student data in cells]
...
```

Each cell shows:
```
ROLL123
CompSci
```

### 6. Updated Room Sheets

**Enhanced**: `_create_room_sheet()`

Added layout information to room summary:
```
Room: Lab 101
Capacity: 60 | Allocated: 58 | Benches: 29
Layout: 8 rows × 4 columns | 4 benches per row
Subject Distribution: Computer Science: 20 | Mathematics: 18 | Physics: 20
```

## Modified Files

1. **backend/services/allocation_service.py**
   - Added `STRICT_MODE` flag
   - Added `_calculate_seat_grid()` method
   - Enhanced `_can_place_subject_at_seat()` with strict checking
   - Updated all three allocation methods:
     - `_allocate_room_advanced()` (mixed strategy)
     - `_allocate_separated_room()` (separated strategy)
     - `_allocate_room_optimal_packing()` (optimal packing strategy)
   - Added grid metadata to all allocations

2. **backend/services/excel_service.py**
   - Enhanced `_create_room_sheet()` with layout info
   - Added `_create_grid_visualization_sheet()` method
   - Each room now generates two sheets: list view + grid view

## How It Works

### Allocation Flow with STRICT_MODE:

1. **Initialize Room**:
   ```
   60-seat room → 30 benches → 8 rows × 4 columns
   ```

2. **For Each Student**:
   - Get primary subject
   - Try each available seat
   - Calculate seat's grid position (row, col, position)
   - Check all allocated students:
     - If same subject + same bench → ❌ Reject
     - If same subject + same column → ❌ Reject
     - If same subject + different column → ✅ Allow
   - Place student if valid

3. **Generate Grid Data**:
   - Each allocation gets grid coordinates
   - Room layout metadata calculated

4. **Excel Output**:
   - List view: Bench-by-bench seating
   - Grid view: Visual room layout

### Example Placement Scenario:

```
Student A (Math) at Seat 1 (Row 0, Col 0, Left)
Student B (Physics) at Seat 2 (Row 0, Col 0, Right) ✅ Different subject, same bench OK
Student C (Math) attempts Seat 2 → ❌ REJECTED (same subject, same bench)
Student C (Math) attempts Seat 9 (Row 1, Col 0, Left) → ❌ REJECTED (same subject, same column)
Student C (Math) attempts Seat 3 (Row 0, Col 1, Left) → ✅ ALLOWED (different column)
```

## Benefits

1. **Enhanced Security**: Much stricter anti-copying measures
2. **Visual Clarity**: Grid view shows exact spatial relationships
3. **Better Planning**: Room layout metadata helps administrators
4. **Compliance Tracking**: Can verify no adjacent same-subject placements
5. **Flexible Rules**: Can toggle STRICT_MODE on/off as needed

## Testing

To test the new features:

1. Start the backend server
2. Create an allocation with any strategy
3. Download the Excel report
4. Check the grid visualization sheets (e.g., "Lab 101_Grid")
5. Verify no same-subject students are:
   - On the same bench (beside each other)
   - In the same column (across from each other)

## Future Enhancements

Possible improvements:
- Configurable benches_per_row (currently fixed at 4)
- Diagonal distance rules
- Subject pairing rules (allow/disallow specific combinations)
- Heat maps showing subject clustering
- Export grid as separate image/PDF
