import sys
sys.path.append('backend')

from models.database import students_collection, rooms_collection, subjects_collection, allocations_collection

print("=" * 80)
print("DATABASE CONTENTS")
print("=" * 80)

students = list(students_collection.find())
print(f"\n📚 STUDENTS: {len(students)} total")
for s in students[:5]:
    subjects_list = s.get('subjects', [s.get('subject', 'N/A')])
    print(f"  • {s['name']} ({s['roll_number']}) - Year {s['year']}")
    print(f"    Subjects: {', '.join(subjects_list)}")
if len(students) > 5:
    print(f"  ... and {len(students)-5} more students")

rooms = list(rooms_collection.find())
print(f"\n🏫 ROOMS: {len(rooms)} total")
for r in rooms:
    print(f"  • {r['name']}: Capacity {r['capacity']} seats")

subjects = list(subjects_collection.find())
print(f"\n📖 SUBJECTS: {len(subjects)} total")
for subj in subjects:
    print(f"  • {subj['name']}")

allocations = list(allocations_collection.find().sort('created_at', -1))
print(f"\n🎯 ALLOCATIONS: {len(allocations)} total")
for i, a in enumerate(allocations[:3], 1):
    summary = a.get('allocation_summary', {})
    print(f"\n  Allocation #{i}:")
    print(f"    Strategy: {a.get('strategy', 'N/A')}")
    print(f"    Subject Filter: {a.get('subject_filter', 'All Subjects') or 'All Subjects'}")
    print(f"    Rooms Used: {summary.get('rooms_used', 0)}")
    print(f"    Students Allocated: {summary.get('total_allocated', 0)}")
    print(f"    Allocation Rate: {summary.get('allocation_percentage', 0)}%")
    print(f"    Quality Rating: {summary.get('quality_rating', 'N/A')}")

    allocs = a.get('allocations', [])
    if allocs:
        print(f"    Room Breakdown:")
        for room_alloc in allocs[:3]:
            room = room_alloc['room']
            student_count = len(room_alloc['students'])
            subjects_in_room = room_alloc.get('subject_breakdown', {})
            print(f"      - {room['name']}: {student_count} students")
            if subjects_in_room:
                print(f"        Subjects: {', '.join([f'{s}({c})' for s, c in subjects_in_room.items()])}")
        if len(allocs) > 3:
            print(f"      ... and {len(allocs)-3} more rooms")

print("\n" + "=" * 80)
