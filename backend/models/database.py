"""
Database models and connection for Exam Seat Allocator
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/exam_allocator')
client = MongoClient(MONGODB_URI)
db = client.exam_allocator

# Collections
students_collection = db.students
rooms_collection = db.rooms
subjects_collection = db.subjects
allocations_collection = db.allocations

def test_connection():
    """Test MongoDB connection"""
    try:
        client.admin.command('ping')
        return True
    except ConnectionFailure:
        raise Exception("Failed to connect to MongoDB")



class Student:
    @staticmethod
    def create(name, roll_number, year, subjects=None, subject=None):
        """Create a new student with multi-subject support"""
        # Handle backward compatibility
        if subjects is None and subject is not None:
            subjects = [subject]
        elif subjects is None:
            subjects = []
        
        student_data = {
            'name': name,
            'roll_number': roll_number,
            'year': year,
            'subjects': subjects,
            'created_at': datetime.utcnow()
        }
        
        # Also store single subject for backward compatibility
        if len(subjects) > 0:
            student_data['subject'] = subjects[0]
        
        result = students_collection.insert_one(student_data)
        return result.inserted_id
    
    @staticmethod
    def get_all():
        """Get all students"""
        return list(students_collection.find({}))
    
    @staticmethod
    def get_by_id(student_id):
        """Get student by ID"""
        return students_collection.find_one({'_id': ObjectId(student_id)})
    
    @staticmethod
    def get_by_subject(subject):
        """Get students by subject (supports both single and multi-subject)"""
        return list(students_collection.find({
            '$or': [
                {'subject': subject},
                {'subjects': subject}
            ]
        }))
    
    @staticmethod
    def get_by_subjects(subjects):
        """Get students who have any of the specified subjects"""
        return list(students_collection.find({
            '$or': [
                {'subject': {'$in': subjects}},
                {'subjects': {'$in': subjects}}
            ]
        }))
    
    @staticmethod
    def update(student_id, **kwargs):
        """Update student"""
        return students_collection.update_one(
            {'_id': ObjectId(student_id)},
            {'$set': kwargs}
        )
    
    @staticmethod
    def delete(student_id):
        """Delete student"""
        return students_collection.delete_one({'_id': ObjectId(student_id)})
    
    @staticmethod
    def delete_by_subject(subject):
        """Delete students by subject"""
        return students_collection.delete_many({
            '$or': [
                {'subject': subject},
                {'subjects': subject}
            ]
        })
    
    @staticmethod
    def get_unique_subjects():
        """Get all unique subjects from students"""
        # Get subjects from both 'subject' and 'subjects' fields
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'single_subjects': {'$addToSet': '$subject'},
                    'multi_subjects': {'$addToSet': '$subjects'}
                }
            }
        ]
        
        result = list(students_collection.aggregate(pipeline))
        if not result:
            return []
        
        subjects = set()
        
        # Add single subjects
        if result[0]['single_subjects']:
            subjects.update([s for s in result[0]['single_subjects'] if s])
        
        # Add multi subjects (flatten the arrays)
        if result[0]['multi_subjects']:
            for subject_list in result[0]['multi_subjects']:
                if subject_list:
                    subjects.update(subject_list)
        
        return sorted(list(subjects))

class Room:
    @staticmethod
    def create(name, capacity):
        """Create a new room"""
        room_data = {
            'name': name,
            'capacity': capacity,
            'created_at': datetime.utcnow()
        }
        result = rooms_collection.insert_one(room_data)
        return result.inserted_id
    
    @staticmethod
    def get_all():
        """Get all rooms"""
        return list(rooms_collection.find({}))
    
    @staticmethod
    def get_by_id(room_id):
        """Get room by ID"""
        return rooms_collection.find_one({'_id': ObjectId(room_id)})
    
    @staticmethod
    def update(room_id, **kwargs):
        """Update room"""
        return rooms_collection.update_one(
            {'_id': ObjectId(room_id)},
            {'$set': kwargs}
        )
    
    @staticmethod
    def delete(room_id):
        """Delete room"""
        return rooms_collection.delete_one({'_id': ObjectId(room_id)})

class Subject:
    @staticmethod
    def create(name):
        """Create a new subject"""
        # Check if subject already exists
        if subjects_collection.find_one({'name': name}):
            return None
        
        subject_data = {
            'name': name,
            'created_at': datetime.utcnow()
        }
        result = subjects_collection.insert_one(subject_data)
        return result.inserted_id
    
    @staticmethod
    def get_all():
        """Get all subjects"""
        return list(subjects_collection.find({}))
    
    @staticmethod
    def get_names():
        """Get all subject names"""
        subjects = subjects_collection.find({}, {'name': 1})
        return [subject['name'] for subject in subjects]
    
    @staticmethod
    def delete_by_name(name):
        """Delete subject by name and associated students"""
        # Delete the subject
        subjects_collection.delete_one({'name': name})
        # Delete students with this subject
        Student.delete_by_subject(name)

class Allocation:
    @staticmethod
    def create(strategy, subject_filter, allocations, allocation_summary):
        """Create a new allocation"""
        allocation_data = {
            'strategy': strategy,
            'subject_filter': subject_filter,
            'allocations': allocations,
            'allocation_summary': allocation_summary,
            'created_at': datetime.utcnow()
        }
        result = allocations_collection.insert_one(allocation_data)
        return result.inserted_id
    
    @staticmethod
    def get_all():
        """Get all allocations"""
        return list(allocations_collection.find({}).sort('created_at', -1))
    
    @staticmethod
    def get_by_id(allocation_id):
        """Get allocation by ID"""
        return allocations_collection.find_one({'_id': ObjectId(allocation_id)})
    
    @staticmethod
    def get_latest():
        """Get the most recent allocation"""
        return allocations_collection.find_one({}, sort=[('created_at', -1)])
    
    @staticmethod
    def delete(allocation_id):
        """Delete allocation"""
        return allocations_collection.delete_one({'_id': ObjectId(allocation_id)})