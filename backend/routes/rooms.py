"""
Room management routes
"""
from flask import Blueprint, request, jsonify
from models.database import Room
from utils.json_utils import serialize_document

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    """Get all rooms"""
    try:
        rooms = Room.get_all()
        return jsonify([serialize_document(room) for room in rooms])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/rooms', methods=['POST'])
def create_room():
    """Create a new room"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'name' not in data or 'capacity' not in data:
            return jsonify({'error': 'Missing required fields: name, capacity'}), 400
        
        room_id = Room.create(
            name=data['name'],
            capacity=int(data['capacity'])
        )
        
        return jsonify({
            'message': 'Room created successfully',
            'room_id': str(room_id)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/rooms/<room_id>', methods=['GET'])
def get_room(room_id):
    """Get a room by ID"""
    try:
        room = Room.get_by_id(room_id)
        if room:
            return jsonify(serialize_document(room))
        return jsonify({'error': 'Room not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/rooms/<room_id>', methods=['PUT'])
def update_room(room_id):
    """Update a room"""
    try:
        data = request.get_json()
        if 'capacity' in data:
            data['capacity'] = int(data['capacity'])
        
        result = Room.update(room_id, **data)
        
        if result.matched_count:
            return jsonify({'message': 'Room updated successfully'})
        return jsonify({'error': 'Room not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/rooms/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    """Delete a room"""
    try:
        result = Room.delete(room_id)
        if result.deleted_count:
            return jsonify({'message': 'Room deleted successfully'})
        return jsonify({'error': 'Room not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
