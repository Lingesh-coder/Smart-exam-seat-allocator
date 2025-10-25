import sys
sys.path.append('backend')

from services.excel_service import ExcelService

test_allocation = {
    'strategy': 'mixed',
    'subject_filter': '',
    'allocation_summary': {
        'total_students': 10,
        'total_allocated': 10,
        'total_unallocated': 0,
        'rooms_used': 2,
        'allocation_percentage': 100,
        'quality_rating': 'Excellent'
    },
    'allocations': [
        {
            'room': {
                'name': 'Lab-1',
                'capacity': 6
            },
            'students': [
                {'seat_number': 1, 'student': {'name': 'John Doe', 'roll_number': 'CS001', 'year': 1, 'subject': 'CS101'}},
                {'seat_number': 2, 'student': {'name': 'Jane Smith', 'roll_number': 'CS002', 'year': 1, 'subject': 'CS101'}},
                {'seat_number': 3, 'student': {'name': 'Bob Johnson', 'roll_number': 'IT001', 'year': 2, 'subject': 'IT201'}},
                {'seat_number': 4, 'student': {'name': 'Alice Brown', 'roll_number': 'IT002', 'year': 2, 'subject': 'IT201'}},
                {'seat_number': 5, 'student': {'name': 'Charlie Davis', 'roll_number': 'CS003', 'year': 1, 'subject': 'CS101'}},
            ],
            'subject_breakdown': {
                'CS101': 3,
                'IT201': 2
            }
        },
        {
            'room': {
                'name': 'IT-201',
                'capacity': 6
            },
            'students': [
                {'seat_number': 1, 'student': {'name': 'Diana Prince', 'roll_number': 'CS004', 'year': 1, 'subject': 'CS101'}},
                {'seat_number': 2, 'student': {'name': 'Eve Adams', 'roll_number': 'IT003', 'year': 2, 'subject': 'IT201'}},
                {'seat_number': 3, 'student': {'name': 'Frank Miller', 'roll_number': 'CS005', 'year': 1, 'subject': 'CS101'}},
                {'seat_number': 4, 'student': {'name': 'Grace Lee', 'roll_number': 'IT004', 'year': 2, 'subject': 'IT201'}},
                {'seat_number': 5, 'student': {'name': 'Henry Wilson', 'roll_number': 'CS006', 'year': 1, 'subject': 'CS101'}},
            ],
            'subject_breakdown': {
                'CS101': 3,
                'IT201': 2
            }
        }
    ]
}

try:
    print("Creating Excel service...")
    excel_service = ExcelService()

    print("Generating allocation report...")
    buffer = excel_service.generate_allocation_report(test_allocation)

    print("Saving to test_allocation_report.xlsx...")
    with open('test_allocation_report.xlsx', 'wb') as f:
        f.write(buffer.getvalue())

    print("✅ Success! Excel file generated: test_allocation_report.xlsx")
    print("\nExpected structure:")
    print("- Summary sheet with allocation statistics")
    print("- Lab-1 sheet with 3 benches (5 students = 2.5 benches, last has only left seat)")
    print("- IT-201 sheet with 3 benches (5 students)")
    print("\nBench layout example:")
    print("Bench 1: Seat 1 (John Doe) | Seat 2 (Jane Smith)")
    print("Bench 2: Seat 3 (Bob Johnson) | Seat 4 (Alice Brown)")
    print("Bench 3: Seat 5 (Charlie Davis) | (empty)")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
