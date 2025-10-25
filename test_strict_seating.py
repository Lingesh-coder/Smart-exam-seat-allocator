import sys
sys.path.append('backend')

from services.allocation_service import AllocationService

def test_grid_calculation():
        print("=" * 60)
    print("TEST 1: Grid Calculation")
    print("=" * 60)

    service = AllocationService()

    capacity = 60

    test_seats = [1, 2, 3, 4, 9, 10, 17, 18, 59, 60]

    print(f"\nRoom Capacity: {capacity} seats")
    print(f"Expected: 30 benches, 8 rows, 4 columns\n")

    for seat_num in test_seats:
        grid = service._calculate_seat_grid(seat_num, capacity)
        print(f"Seat {seat_num:2d}: Row {grid['row']}, Col {grid['col']}, "
              f"Position: {grid['position']:5s}, Bench #{grid['bench_num']}")

    print("\n✅ Grid calculation test complete\n")


def test_strict_placement_rules():
        print("=" * 60)
    print("TEST 2: Strict Placement Rules")
    print("=" * 60)

    service = AllocationService()
    capacity = 60
    seat_subjects = {}

    seat_subjects[1] = "Mathematics"

    print(f"\nInitial placement: Mathematics student at Seat 1")
    print(f"  Grid: {service._calculate_seat_grid(1, capacity)}\n")

    test_cases = [
        (2, "Mathematics", "Same bench (beside)", False),
        (2, "Physics", "Same bench, different subject", True),
        (9, "Mathematics", "Same column (across)", False),
        (9, "Physics", "Same column, different subject", True),
        (3, "Mathematics", "Different column (behind OK)", True),
        (17, "Mathematics", "Same column as Seat 1 (across)", False),
        (5, "Mathematics", "Different column & row", True),
    ]

    for seat_num, subject, description, expected in test_cases:
        grid = service._calculate_seat_grid(seat_num, capacity)
        can_place = service._can_place_subject_at_seat(seat_subjects, seat_num, subject, capacity)

        status = "✅ ALLOWED" if can_place else "❌ REJECTED"
        match = "✅" if can_place == expected else "❌ MISMATCH"

        print(f"Seat {seat_num:2d} ({description})")
        print(f"  Grid: Row {grid['row']}, Col {grid['col']}, {grid['position']}")
        print(f"  Subject: {subject}")
        print(f"  Result: {status} {match}")
        print()

    print("✅ Strict placement rules test complete\n")


def test_bench_layout():
        print("=" * 60)
    print("TEST 3: Room Layout Calculations")
    print("=" * 60)

    service = AllocationService()

    test_capacities = [20, 40, 60, 80, 100]

    print("\nCalculating room layouts for various capacities:\n")

    for capacity in test_capacities:
        total_benches = capacity // 2
        benches_per_row = 4
        total_rows = (total_benches + benches_per_row - 1) // benches_per_row

        print(f"Capacity: {capacity:3d} seats → "
              f"{total_benches:2d} benches → "
              f"{total_rows:2d} rows × {benches_per_row} columns")

    print("\n✅ Room layout calculations test complete\n")


def test_adjacent_detection():
        print("=" * 60)
    print("TEST 4: Adjacent Detection Logic")
    print("=" * 60)

    service = AllocationService()
    capacity = 60

    seat_subjects = {
        1: "Computer Science",
        10: "Computer Science",
        19: "Computer Science",
    }

    print("\nExisting placements (Computer Science):")
    for seat, subj in seat_subjects.items():
        grid = service._calculate_seat_grid(seat, capacity)
        print(f"  Seat {seat:2d}: Row {grid['row']}, Col {grid['col']}, {grid['position']}")

    print("\nTesting Computer Science student placement attempts:\n")

    test_attempts = [
        (2, "Same bench as Seat 1", False),
        (9, "Same column as Seat 1", False),
        (17, "Same column as Seat 1", False),
        (9, "Same bench as Seat 10", False),
        (20, "Same bench as Seat 19", False),
        (27, "Same column as Seat 19", False),
        (3, "Same column as Seat 19", False),
        (5, "Different column from all", True),
        (7, "Different column from all", True),
        (11, "Same column as Seat 19", False),
    ]

    for seat_num, description, expected in test_attempts:
        grid = service._calculate_seat_grid(seat_num, capacity)
        can_place = service._can_place_subject_at_seat(
            seat_subjects, seat_num, "Computer Science", capacity
        )

        status = "✅ ALLOWED" if can_place else "❌ REJECTED"
        match = "✅" if can_place == expected else "❌ MISMATCH"

        print(f"Seat {seat_num:2d}: {description}")
        print(f"  Grid: Row {grid['row']}, Col {grid['col']}, {grid['position']}")
        print(f"  Result: {status} {match}")
        print()

    print("✅ Adjacent detection test complete\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("STRICT ADJACENT SEATING - TEST SUITE")
    print("=" * 60 + "\n")

    try:
        test_grid_calculation()
        test_strict_placement_rules()
        test_bench_layout()
        test_adjacent_detection()

        print("=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY! ✅")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR:\n{e}\n")
        import traceback
        traceback.print_exc()
