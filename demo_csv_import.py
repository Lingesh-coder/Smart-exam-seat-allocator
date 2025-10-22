#!/usr/bin/env python3
"""
Demo script to test CSV import functionality
This script demonstrates how to use the CSV import endpoints programmatically
"""

import requests
import json

# Configuration
API_BASE_URL = 'http://localhost:5000/api'

def read_csv_file(filepath):
    """Read CSV file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return None

def upload_csv_data(endpoint, csv_content, data_type):
    """Upload CSV data to the specified endpoint"""
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    data = {'csv_content': csv_content}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ {data_type} import successful:")
            print(f"   - Created: {result.get('created_count', 0)}")
            print(f"   - Total rows: {result.get('total_rows', 0)}")
            print(f"   - Message: {result.get('message', 'Success')}")
            
            if 'errors' in result:
                print(f"   - Errors: {len(result['errors'])}")
                for error in result['errors'][:3]:  # Show first 3 errors
                    print(f"     • {error}")
                if len(result['errors']) > 3:
                    print(f"     • ... and {len(result['errors']) - 3} more")
            
            return True
        else:
            error_data = response.json()
            print(f"❌ {data_type} import failed:")
            print(f"   - Status: {response.status_code}")
            print(f"   - Error: {error_data.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error: Make sure the backend server is running on {API_BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def get_sample_csv(endpoint, data_type):
    """Get sample CSV from the API"""
    url = f"{API_BASE_URL}/{endpoint}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            sample_csv = result.get('sample_csv', '')
            print(f"📄 {data_type} sample CSV:")
            print(sample_csv)
            print("-" * 50)
            return sample_csv
        else:
            print(f"❌ Failed to get {data_type} sample CSV")
            return None
            
    except Exception as e:
        print(f"❌ Error getting sample CSV: {str(e)}")
        return None

def demo_csv_import():
    """Demonstrate CSV import functionality"""
    
    print("🚀 CSV Import Demo")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Backend server is not responding properly")
            return
    except:
        print("❌ Cannot connect to backend server. Make sure it's running on http://localhost:5000")
        return
    
    print("✅ Backend server is running")
    print()
    
    # Test 1: Get sample CSV data
    print("📋 Step 1: Getting sample CSV data")
    subjects_sample = get_sample_csv('subjects/csv/sample', 'Subjects')
    rooms_sample = get_sample_csv('rooms/csv/sample', 'Rooms')
    students_sample = get_sample_csv('students/csv/sample', 'Students')
    
    print()
    
    # Test 2: Import sample data
    print("📤 Step 2: Importing sample data")
    
    # Import subjects first
    if subjects_sample:
        upload_csv_data('subjects/csv/upload', subjects_sample, 'Subjects')
        print()
    
    # Import rooms
    if rooms_sample:
        upload_csv_data('rooms/csv/upload', rooms_sample, 'Rooms')
        print()
    
    # Import students
    if students_sample:
        upload_csv_data('students/csv/upload', students_sample, 'Students')
        print()
    
    # Test 3: Try importing from files (if they exist)
    print("📁 Step 3: Importing from sample files (if available)")
    
    sample_files = [
        ('sample-data/subjects_sample.csv', 'subjects/csv/upload', 'Subjects'),
        ('sample-data/rooms_sample.csv', 'rooms/csv/upload', 'Rooms'),
        ('sample-data/students_sample.csv', 'students/csv/upload', 'Students')
    ]
    
    for filepath, endpoint, data_type in sample_files:
        csv_content = read_csv_file(filepath)
        if csv_content:
            print(f"📄 Importing {data_type} from {filepath}")
            upload_csv_data(endpoint, csv_content, data_type)
            print()
        else:
            print(f"⏭️  Skipping {filepath} (file not found)")
    
    print("🎉 Demo completed!")
    print("\nNext steps:")
    print("1. Open the web application at http://localhost:5174")
    print("2. Check that your data has been imported")
    print("3. Try the CSV upload interface in the web app")
    print("4. Test seat allocation with the imported data")

if __name__ == "__main__":
    demo_csv_import()