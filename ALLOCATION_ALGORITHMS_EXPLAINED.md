# Three Seating Allocation Algorithms Explained

## Current Database State

### Statistics
- **Students**: 620 total
- **Rooms**: 20 total (capacity ranges from 35-50 seats each)
- **Subjects**: 8 total (CS101, CS201, CS301, IT101, IT201, IT301, MATH101, MATH201)
- **Total Capacity**: ~920 seats
- **Allocations Created**: 40 (using different strategies)

---

## Algorithm 1: MIXED STRATEGY (Minimize Rooms)

### 🎯 Goal
Fill rooms sequentially to minimize the number of rooms used while ensuring same subjects are separated within each room.

### 📋 How It Works

1. **Group Students by Subject**
   ```
   CS101 → [Student1, Student2, Student3, ...]
   IT201 → [Student4, Student5, ...]
   ```

2. **Shuffle Each Subject Group**
   - Randomize order within each subject to prevent predictable patterns

3. **Calculate Subject Distribution**
   - Determine how many students of each subject should go in each room
   - Uses proportional distribution based on subject sizes

4. **Fill Rooms Sequentially (Largest First)**
   - Room 1: Fill to capacity, mixing subjects
   - Room 2: Fill to capacity, mixing subjects
   - Continue until all students allocated

5. **Anti-Copying Mechanism**
   - **Minimum Distance**: 2 seats between same subjects
   - **Preferred Distance**: 3 seats (tries for this first)
   - **Spatial Calculation**: Uses 2D grid (rows × columns)
   ```
   Seat Grid Example (6 capacity):
   Row 0: [1, 2, 3]
   Row 1: [4, 5, 6]
   
   If CS101 in seat 1, next CS101 must be at least seat 3 or later
   ```

### 📊 Example Result (from your database)
```
Room: CS Lab 3 (50 capacity)
  IT101: 10 students  (20%)
  CS201: 8 students   (16%)
  CS301: 8 students   (16%)
  IT301: 8 students   (16%)
  CS101: 8 students   (16%)
  IT201: 8 students   (16%)
```

### ✅ Advantages
- **Efficient**: Uses minimum rooms (13 rooms for 620 students)
- **Balanced**: Good subject mix in each room
- **Quality**: Excellent rating (good separation achieved)

### ❌ Disadvantages
- Large rooms get very crowded
- Some rooms might be completely full while others empty

---

## Algorithm 2: SEPARATED STRATEGY (Maximum Subject Separation)

### 🎯 Goal
Distribute same subjects across DIFFERENT rooms to maximize physical separation between students taking the same exam.

### 📋 How It Works

1. **Group Students by Subject**
   ```
   CS101 → 155 students
   IT101 → 155 students
   etc.
   ```

2. **Calculate Room Distribution**
   - If subject has ≤ number of rooms: Put one student per room
   - If subject has > number of rooms: Split proportionally
   ```
   Example:
   CS101 (155 students) across 20 rooms
   = ~7-8 students per room
   ```

3. **Assign Subjects to Rooms (Round-Robin)**
   ```
   Room 1: CS101(7), IT101(7), CS201(5), ...
   Room 2: CS101(7), IT101(7), CS201(5), ...
   Room 3: CS101(7), IT101(7), CS201(5), ...
   ```

4. **Allocate Within Room**
   - Uses same anti-copying distance rules
   - But now same subjects are already split across rooms

### 📊 Example Result (from your database)
```
Room: Main Hall A (31 students - NOT full!)
  IT201: 5 students
  CS101: 6 students
  IT101: 6 students
  CS201: 5 students
  CS301: 5 students
  IT301: 4 students
```

### ✅ Advantages
- **Maximum Separation**: Same subjects rarely in same room
- **Fair Distribution**: All rooms get students
- **Quality**: Excellent rating (best anti-copying)
- **Smaller Groups**: Each room less crowded

### ❌ Disadvantages
- **Inefficient**: Uses ALL 20 rooms (vs 13 in mixed)
- **Wasted Space**: Rooms not filled to capacity (31/50 = 62%)
- **More Supervisors**: Need staff for every room

---

## Algorithm 3: OPTIMAL PACKING (Minimize Wasted Space)

### 🎯 Goal
Pack students as tightly as possible into fewest rooms while maintaining decent separation.

### 📋 How It Works

1. **Sort Rooms by Capacity (Largest First)**
   ```
   [50, 50, 50, 49, 48, 48, 47, ...]
   ```

2. **Create Round-Robin Student Pool**
   ```
   Round 1: CS101(1), IT101(1), CS201(1), ...
   Round 2: CS101(2), IT101(2), CS201(2), ...
   Shuffle after each round
   Final shuffle of entire pool
   ```
   This prevents subject clustering

3. **Fill Rooms Completely**
   - Take next N students from pool (N = room capacity)
   - Try to place with minimum distance rules
   - If can't maintain distance, compromise and place anyway

4. **Emergency Fill**
   - If seats remain and students waiting, fill without distance rules
   - Goal is 100% allocation, even if some same-subjects sit close

### 📊 Example Result (from your database)
```
Room: Main Hall A (50 students - FULL!)
  IT201: 11 students  (22%)
  CS201: 7 students   (14%)
  IT101: 11 students  (22%)
  CS101: 8 students   (16%)
  IT301: 9 students   (18%)
  CS301: 4 students   (8%)
```

### ✅ Advantages
- **Most Efficient**: Only 13 rooms used (same as mixed)
- **100% Capacity**: Rooms filled completely (50/50)
- **No Waste**: Minimal empty seats
- **Complete Allocation**: Guaranteed all students get seats

### ❌ Disadvantages
- **Lower Quality**: "Needs Improvement" rating
- **Compromised Separation**: Distance rules relaxed to fill
- **Clustered Subjects**: Some same-subjects may sit too close

---

## Comparison Table

| Feature | Mixed | Separated | Optimal Packing |
|---------|-------|-----------|-----------------|
| **Rooms Used** | 13 | 20 | 13 |
| **Avg Room Fill** | ~48/50 (96%) | ~31/50 (62%) | 50/50 (100%) |
| **Quality Rating** | Excellent | Excellent | Needs Improvement |
| **Anti-Copying** | Good | Best | Fair |
| **Space Efficiency** | High | Low | Highest |
| **Same-Subject Distance** | 2-3 seats | Multiple rooms | 0-2 seats |
| **Best For** | General exams | High-security exams | Limited rooms |

---

## Key Parameters Used by All Algorithms

```python
MIN_DISTANCE = 2         # Minimum seats between same subjects
MAX_ATTEMPTS = 1000      # Retry limit for seat placement
PREFERRED_DISTANCE = 3   # Ideal separation (tries this first)
```

### Distance Calculation
```python
# Linear distance between seat numbers
distance = abs(seat2 - seat1)

# Spatial distance in 2D grid
row1 = (seat1 - 1) // cols
col1 = (seat1 - 1) % cols
row2 = (seat2 - 1) // cols
col2 = (seat2 - 1) % cols
spatial_distance = sqrt((row2-row1)² + (col2-col1)²)
```

---

## When to Use Each Strategy

### Use MIXED When:
- ✅ You want balanced rooms
- ✅ You need efficient space usage
- ✅ You have enough rooms for comfort
- ✅ Anti-copying is important but not critical

### Use SEPARATED When:
- ✅ High-stakes exams (finals, board exams)
- ✅ Maximum anti-copying needed
- ✅ You have plenty of rooms
- ✅ Budget for many supervisors
- ✅ Willing to "waste" space for security

### Use OPTIMAL PACKING When:
- ✅ Limited rooms available
- ✅ Must accommodate all students
- ✅ Space efficiency is priority
- ✅ Anti-copying is secondary concern
- ✅ Multiple exam sessions (save rooms for later)

---

## Your Current Best Allocation

Looking at your database, the **SEPARATED strategy** achieved:
- ✅ 100% allocation rate
- ✅ Excellent quality rating
- ✅ Best anti-copying measures
- ✅ Fair distribution across all rooms

But if you need to minimize rooms, **MIXED strategy** is equally good:
- ✅ Only 13 rooms (vs 20)
- ✅ Still Excellent quality
- ✅ 100% allocation
- ✅ Good subject mixing

**OPTIMAL PACKING** sacrificed quality for efficiency:
- ❌ "Needs Improvement" rating
- ✅ But 100% room fill rate
- ✅ Maximum space efficiency
