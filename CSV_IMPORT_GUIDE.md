# CSV Import Feature - User Guide

## Overview

The Exam Seat Allocator now supports bulk import of data through CSV files. You can import students, rooms, and subjects quickly using properly formatted CSV files.

## Features Added

### 1. CSV Upload Interface
- **Location**: Main application → "Show CSV Import" button
- **Functionality**: Upload CSV files or paste CSV content directly
- **File Types Supported**: Students, Rooms, Subjects

### 2. Drag & Drop Support
- Drag CSV files directly onto the upload areas
- Visual feedback during drag operations
- Automatic file type validation

### 3. Sample Data Generation
- Download sample CSV templates
- See correct formatting examples
- Use dummy data for testing

### 4. Error Handling & Validation
- Real-time feedback on import status
- Detailed error messages for invalid data
- Import summary with success/failure counts

## CSV Format Requirements

### Students CSV
```csv
name,roll_number,year,subjects
John Doe,CS001,1,"CS101,MATH101"
Jane Smith,CS002,2,"IT201,DB201"
```

**Required Columns:**
- `name`: Student full name
- `roll_number`: Unique student identifier  
- `year`: Academic year (1, 2, 3, or 4)
- `subjects`: Comma-separated subject codes (in quotes)

**Alternative Column Names:**
- Name: `student_name`, `student name`
- Roll Number: `roll number`, `roll_no`, `rollno`, `id`
- Year: `class`, `semester`
- Subjects: `subject`, `courses`, `course`

### Rooms CSV
```csv
name,capacity
Lab-1,30
Conference Room,20
```

**Required Columns:**
- `name`: Room name/identifier
- `capacity`: Maximum number of seats (must be positive integer)

**Alternative Column Names:**
- Name: `room_name`, `room name`, `room`
- Capacity: `seats`, `size`, `max_capacity`

### Subjects CSV
```csv
name
CS101
MATH101
IT201
```

**Required Columns:**
- `name`: Subject code or name

**Alternative Column Names:**
- Name: `subject_name`, `subject name`, `subject`, `code`, `subject_code`

## How to Use

### Method 1: File Upload
1. Click "Show CSV Import" in the main application
2. Choose the appropriate section (Students, Rooms, or Subjects)
3. Click "Choose File" and select your CSV file
4. Review the loaded data
5. Click "Upload Data" to import

### Method 2: Drag & Drop
1. Prepare your CSV file
2. Drag the file onto the appropriate upload area
3. Review the loaded data
4. Click "Upload Data" to import

### Method 3: Direct Paste
1. Click "Paste CSV" in any upload section
2. Copy your CSV content and paste it in the text area
3. Click "Upload Data" to import

### Method 4: Sample Data
1. Use the provided sample files in `sample-data/` directory
2. Or download sample templates using "Sample CSV" buttons
3. Modify the sample data as needed
4. Import using any of the above methods

## Sample Data Files

The `sample-data/` directory contains ready-to-use CSV files:

- **students_sample.csv**: 20 students across 4 years with realistic subject combinations
- **rooms_sample.csv**: 15 rooms with varying capacities (15-100 seats)
- **subjects_sample.csv**: 44 subjects covering CS/IT curriculum

## Import Process & Validation

### Validation Rules
1. **Students**:
   - Name and roll number are required
   - Year must be 1-4
   - At least one subject must be specified
   - Roll numbers should be unique

2. **Rooms**:
   - Name and capacity are required
   - Capacity must be a positive integer
   - Room names should be unique

3. **Subjects**:
   - Subject name is required
   - Subject names should be unique

### Error Handling
- Invalid rows are skipped with detailed error messages
- Successful imports are reported with counts
- Partial imports are supported (some rows succeed, others fail)
- Duplicate detection and handling

### Data Relationships
- Import subjects first to establish the subject catalog
- Import rooms to define available venues
- Import students last (they reference subjects)
- Students can have multiple subjects
- Allocation algorithms work with imported data

## Tips for Best Results

1. **Data Preparation**:
   - Use consistent naming conventions
   - Ensure roll numbers are unique
   - Verify room capacities are realistic
   - Check subject codes match across students

2. **Import Order**:
   - Import subjects first
   - Import rooms second  
   - Import students last

3. **Testing**:
   - Start with sample data to verify functionality
   - Test with small datasets first
   - Verify data appears correctly after import

4. **Troubleshooting**:
   - Check CSV formatting if imports fail
   - Ensure required columns are present
   - Verify data types (especially numeric fields)
   - Use sample templates as reference

## Technical Implementation

### Backend Endpoints
- `POST /api/students/csv/upload`: Import students from CSV
- `POST /api/rooms/csv/upload`: Import rooms from CSV  
- `POST /api/subjects/csv/upload`: Import subjects from CSV
- `GET /api/*/csv/sample`: Download sample CSV templates

### Frontend Components
- `CSVUploader`: Reusable upload component with drag/drop
- Integrated validation and status reporting
- Real-time feedback during import process

### CSV Processing
- Uses Python's built-in `csv` module
- Flexible column name mapping
- Comprehensive error handling and validation
- Batch processing with individual row error tracking

## Integration with Existing Features

The CSV import feature seamlessly integrates with existing functionality:

- **Seat Allocation**: Imported data immediately available for allocation
- **PDF Reports**: Works with imported student and room data
- **Manual Entry**: Can mix CSV imports with manual data entry
- **Data Management**: All CRUD operations work with imported data

This feature significantly speeds up the setup process for exam seat allocation, especially when dealing with large numbers of students, rooms, or subjects.