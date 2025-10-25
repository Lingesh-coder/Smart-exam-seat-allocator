import csv
import io
from typing import List, Dict, Any

def parse_csv_content(csv_content: str, file_type: str) -> List[Dict[str, Any]]:
    try:
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        data = []

        for row_num, row in enumerate(csv_reader, start=2):
            if file_type == 'students':
                parsed_row = parse_student_row(row, row_num)
            elif file_type == 'rooms':
                parsed_row = parse_room_row(row, row_num)
            elif file_type == 'subjects':
                parsed_row = parse_subject_row(row, row_num)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            if parsed_row:
                data.append(parsed_row)

        return data

    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def parse_student_row(row: Dict[str, str], row_num: int) -> Dict[str, Any]:
    clean_row = {k.strip().lower(): v.strip() for k, v in row.items() if v.strip()}

    if not clean_row:
        return None

    name_keys = ['name', 'student_name', 'student name']
    roll_keys = ['roll_number', 'roll number', 'roll_no', 'rollno', 'id']
    year_keys = ['year', 'class', 'semester']
    subject_keys = ['subjects', 'subject', 'courses', 'course']

    name = None
    for key in name_keys:
        if key in clean_row:
            name = clean_row[key]
            break

    roll_number = None
    for key in roll_keys:
        if key in clean_row:
            roll_number = clean_row[key]
            break

    year = None
    for key in year_keys:
        if key in clean_row:
            year_str = clean_row[key]
            if year_str.isdigit():
                year = int(year_str)
            elif 'year' in year_str.lower():
                for char in year_str:
                    if char.isdigit():
                        year = int(char)
                        break
            break

    subjects = []
    for key in subject_keys:
        if key in clean_row:
            subject_str = clean_row[key]
            subjects = [s.strip() for s in subject_str.split(',') if s.strip()]
            break

    if not name:
        raise ValueError(f"Row {row_num}: Missing student name")
    if not roll_number:
        raise ValueError(f"Row {row_num}: Missing roll number")
    if not year:
        raise ValueError(f"Row {row_num}: Missing or invalid year")
    if not subjects:
        raise ValueError(f"Row {row_num}: Missing subjects")

    return {
        'name': name,
        'roll_number': roll_number,
        'year': year,
        'subjects': subjects
    }

def parse_room_row(row: Dict[str, str], row_num: int) -> Dict[str, Any]:
    clean_row = {k.strip().lower(): v.strip() for k, v in row.items() if v.strip()}

    if not clean_row:
        return None

    name_keys = ['name', 'room_name', 'room name', 'room']
    capacity_keys = ['capacity', 'seats', 'size', 'max_capacity']

    name = None
    for key in name_keys:
        if key in clean_row:
            name = clean_row[key]
            break

    capacity = None
    for key in capacity_keys:
        if key in clean_row:
            capacity_str = clean_row[key]
            try:
                capacity = int(capacity_str)
            except ValueError:
                raise ValueError(f"Row {row_num}: Invalid capacity '{capacity_str}' - must be a number")
            break

    if not name:
        raise ValueError(f"Row {row_num}: Missing room name")
    if capacity is None:
        raise ValueError(f"Row {row_num}: Missing capacity")
    if capacity <= 0:
        raise ValueError(f"Row {row_num}: Capacity must be greater than 0")
    if capacity > 50:
        raise ValueError(f"Row {row_num}: Capacity cannot exceed 50 seats")

    return {
        'name': name,
        'capacity': capacity
    }

def parse_subject_row(row: Dict[str, str], row_num: int) -> Dict[str, Any]:
    clean_row = {k.strip().lower(): v.strip() for k, v in row.items() if v.strip()}

    if not clean_row:
        return None

    name_keys = ['name', 'subject_name', 'subject name', 'subject', 'code', 'subject_code']

    name = None
    for key in name_keys:
        if key in clean_row:
            name = clean_row[key]
            break

    if not name:
        raise ValueError(f"Row {row_num}: Missing subject name")

    return {
        'name': name
    }

def generate_sample_csv(file_type: str) -> str:
    if file_type == 'students':
        return """name,roll_number,year,subjects
John Doe,2021001,1,Mathematics
Jane Smith,2021002,2,"Physics,Chemistry"
Bob Johnson,2021003,1,Computer Science"""
    elif file_type == 'rooms':
        return """name,capacity
Room A,30
Room B,40
Room C,50"""
    elif file_type == 'subjects':
        return """name
Mathematics
Physics
Chemistry
Computer Science"""
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
