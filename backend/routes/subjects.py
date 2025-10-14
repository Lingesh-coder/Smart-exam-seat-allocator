"""
Subject management routes
"""
from flask import Blueprint, request, jsonify
from models.database import Subject
from utils.json_utils import serialize_document

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
