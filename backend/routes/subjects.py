"""
Subject management routes
"""
from flask import Blueprint, request, jsonify
from models.database import Subject
from utils.json_utils import serialize_document
from utils.csv_utils import parse_csv_content, generate_sample_csv

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('/subjects', methods=['GET'])
def get_subjects():
    """Get all subjects"""
    try:
        subjects = Subject.get_all()
        return jsonify([serialize_document(subject) for subject in subjects])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subjects_bp.route('/subjects/names', methods=['GET'])
def get_subject_names():
    """Get all subject names"""
    try:
        names = Subject.get_names()
        return jsonify(names)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subjects_bp.route('/subjects', methods=['POST'])
def create_subject():
    """Create a new subject"""
    try:
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({'error': 'Missing required field: name'}), 400
        
        subject_id = Subject.create(data['name'])
        
        if subject_id is None:
            return jsonify({'error': 'Subject already exists'}), 400
        
        return jsonify({
            'message': 'Subject created successfully',
            'subject_id': str(subject_id)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subjects_bp.route('/subjects/<name>', methods=['DELETE'])
def delete_subject(name):
    """Delete a subject by name"""
    try:
        Subject.delete_by_name(name)
        return jsonify({'message': 'Subject and associated students deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subjects_bp.route('/subjects/csv/upload', methods=['POST'])
def upload_subjects_csv():
    """Upload subjects from CSV file"""
    try:
        data = request.get_json()
        
        if 'csv_content' not in data:
            return jsonify({'error': 'Missing CSV content'}), 400
        
        # Parse CSV content
        subjects_data = parse_csv_content(data['csv_content'], 'subjects')
        
        if not subjects_data:
            return jsonify({'error': 'No valid subject data found in CSV'}), 400
        
        # Create subjects
        created_count = 0
        errors = []
        
        for subject_data in subjects_data:
            try:
                subject_id = Subject.create(subject_data['name'])
                if subject_id is not None:
                    created_count += 1
                else:
                    errors.append(f"Subject {subject_data['name']} already exists")
            except Exception as e:
                errors.append(f"Error creating subject {subject_data.get('name', 'Unknown')}: {str(e)}")
        
        response = {
            'message': f'Successfully imported {created_count} subjects',
            'created_count': created_count,
            'total_rows': len(subjects_data)
        }
        
        if errors:
            response['errors'] = errors
        
        return jsonify(response), 201 if created_count > 0 else 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subjects_bp.route('/subjects/csv/sample', methods=['GET'])
def get_subjects_csv_sample():
    """Get sample CSV format for subjects"""
    try:
        sample_csv = generate_sample_csv('subjects')
        return jsonify({'sample_csv': sample_csv})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subjects_bp.route('/subjects/all', methods=['DELETE'])
def delete_all_subjects():
    """Delete all subjects"""
    try:
        result = Subject.delete_all()
        return jsonify({
            'message': f'Successfully deleted {result.deleted_count} subjects',
            'deleted_count': result.deleted_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
