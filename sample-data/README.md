# Sample CSV Data for Exam Seat Allocator

This directory contains sample CSV files that can be used to quickly populate the exam seat allocator with dummy data.

## Files Included

### 1. students_sample.csv
Contains 20 sample students with their details:
- **Columns**: name, roll_number, year, subjects
- **Example**: `John Doe,CS001,1,"CS101,MATH101,PHYS101"`
- Students from years 1-4 with realistic subject combinations

### 2. rooms_sample.csv
Contains 15 sample rooms with varying capacities:
- **Columns**: name, capacity
- **Example**: `Lab-1,30`
- Mix of labs, lecture halls, and seminar rooms

### 3. subjects_sample.csv
Contains 44 sample subjects covering CS and IT curriculum:
- **Columns**: name
- **Example**: `CS101`
- Subjects organized by year level (101, 201, 301, 401)

## How to Use

1. **In the Application**:
   - Click "Show CSV Import" in the main application
   - Use the CSV uploaders to import data
   - Download sample templates to see the expected format

2. **Manual Import**:
   - Copy the content from these files
   - Paste into the CSV text areas in the application
   - Click "Upload Data"

3. **File Upload**:
   - Save these files to your computer
   - Use the file upload feature in the application

## CSV Format Notes

### Students CSV
- **subjects**: Multiple subjects should be comma-separated and enclosed in quotes
- **year**: Numeric value (1, 2, 3, or 4)
- **roll_number**: Unique identifier for each student

### Rooms CSV
- **capacity**: Numeric value representing maximum seats
- **name**: Unique room identifier

### Subjects CSV
- **name**: Unique subject code/name
- Follow standard academic naming conventions

## Data Relationships

The sample data is designed with realistic relationships:
- Year 1 students take foundational courses (101 level)
- Year 2-3 students take intermediate courses (201-301 level)  
- Year 4 students take advanced/capstone courses (401 level)
- Room capacities range from 15-100 to accommodate different class sizes

## Quick Start

To quickly populate your system with all sample data:

1. Import subjects first (establishes the subject catalog)
2. Import rooms (establishes available venues)
3. Import students (who reference the subjects)
4. Run seat allocation with your preferred strategy

This will give you a realistic dataset to test the seat allocation algorithms and PDF report generation.