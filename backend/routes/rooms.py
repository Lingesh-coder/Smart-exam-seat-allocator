"""
Room management routes
"""
from flask import Blueprint, request, jsonify
from models.database import Room
from utils.json_utils import serialize_document
from utils.csv_utils import parse_csv_content, generate_sample_csv

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

@rooms_bp.route('/rooms/csv/upload', methods=['POST'])
def upload_rooms_csv():
    """Upload rooms from CSV file"""
    try:
        data = request.get_json()
        
        if 'csv_content' not in data:
            return jsonify({'error': 'Missing CSV content'}), 400
        
        # Parse CSV content
        rooms_data = parse_csv_content(data['csv_content'], 'rooms')
        
        if not rooms_data:
            return jsonify({'error': 'No valid room data found in CSV'}), 400
        
        # Create rooms
        created_count = 0
        errors = []
        
        for room_data in rooms_data:
            try:
                Room.create(
                    name=room_data['name'],
                    capacity=room_data['capacity']
                )
                created_count += 1
            except Exception as e:
                errors.append(f"Error creating room {room_data.get('name', 'Unknown')}: {str(e)}")
        
        response = {
            'message': f'Successfully imported {created_count} rooms',
            'created_count': created_count,
            'total_rows': len(rooms_data)
        }
        
        if errors:
            response['errors'] = errors
        
        return jsonify(response), 201 if created_count > 0 else 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rooms_bp.route('/rooms/csv/sample', methods=['GET'])
def get_rooms_csv_sample():
    """Get sample CSV format for rooms"""
    try:
        sample_csv = generate_sample_csv('rooms')
        return jsonify({'sample_csv': sample_csv})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
