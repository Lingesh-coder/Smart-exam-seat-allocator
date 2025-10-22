"""
Student management routes
"""
from flask import Blueprint, request, jsonify
from models.database import Student
from utils.json_utils import serialize_document
from utils.csv_utils import parse_csv_content, generate_sample_csv

students_bp = Blueprint('students', __name__)

@students_bp.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        students = Student.get_all()
        return jsonify([serialize_document(student) for student in students])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/students', methods=['POST'])
def create_student():
    """Create a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'roll_number', 'year']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Handle subjects (multi-subject support)
        subjects = data.get('subjects', [])
        if not subjects and 'subject' in data:
            subjects = [data['subject']]
        
        student_id = Student.create(
            name=data['name'],
            roll_number=data['roll_number'],
            year=data['year'],
            subjects=subjects
        )
        
        return jsonify({
            'message': 'Student created successfully',
            'student_id': str(student_id)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get a student by ID"""
    try:
        student = Student.get_by_id(student_id)
        if student:
            return jsonify(serialize_document(student))
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student"""
    try:
        data = request.get_json()
        result = Student.update(student_id, **data)
        
        if result.matched_count:
            return jsonify({'message': 'Student updated successfully'})
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    try:
        result = Student.delete(student_id)
        if result.deleted_count:
            return jsonify({'message': 'Student deleted successfully'})
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/students/subjects', methods=['GET'])
def get_student_subjects():
    """Get unique subjects from students"""
    try:
        subjects = Student.get_unique_subjects()
        return jsonify(subjects)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/students/csv/upload', methods=['POST'])
def upload_students_csv():
    """Upload students from CSV file"""
    try:
        data = request.get_json()
        
        if 'csv_content' not in data:
            return jsonify({'error': 'Missing CSV content'}), 400
        
        # Parse CSV content
        students_data = parse_csv_content(data['csv_content'], 'students')
        
        if not students_data:
            return jsonify({'error': 'No valid student data found in CSV'}), 400
        
        # Create students
        created_count = 0
        errors = []
        
        for student_data in students_data:
            try:
                Student.create(
                    name=student_data['name'],
                    roll_number=student_data['roll_number'],
                    year=student_data['year'],
                    subjects=student_data['subjects']
                )
                created_count += 1
            except Exception as e:
                errors.append(f"Error creating student {student_data.get('name', 'Unknown')}: {str(e)}")
        
        response = {
            'message': f'Successfully imported {created_count} students',
            'created_count': created_count,
            'total_rows': len(students_data)
        }
        
        if errors:
            response['errors'] = errors
        
        return jsonify(response), 201 if created_count > 0 else 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/students/csv/sample', methods=['GET'])
def get_students_csv_sample():
    """Get sample CSV format for students"""
    try:
        sample_csv = generate_sample_csv('students')
        return jsonify({'sample_csv': sample_csv})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
