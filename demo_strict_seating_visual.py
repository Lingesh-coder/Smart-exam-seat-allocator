import sys
sys.path.append('backend')

from services.allocation_service import AllocationService


def visualize_room_grid():

    print("\n" + "=" * 80)
    print("VISUAL DEMONSTRATION: Strict Seating Grid Layout")
    print("=" * 80 + "\n")

    service = AllocationService()
    capacity = 32

    print(f"Room Setup: {capacity} seats")
    print(f"  • {capacity // 2} benches (2 students per bench)")
    print(f"  • 4 rows × 4 columns")
    print(f"  • STRICT_MODE: {service.STRICT_MODE}")
    print()

    seat_subjects = {}
    grid_display = {}

    for row in range(4):
        grid_display[row] = {}
        for col in range(4):
            grid_display[row][col] = {'left': None, 'right': None}

    placements = [
        (1, "Math", "Alice"),
        (11, "Math", "Bob"),
        (22, "Math", "Carol"),
    ]

    print("Initial Placements (Math students):")
    print("-" * 80)

    for seat_num, subject, name in placements:
        seat_subjects[seat_num] = subject
        grid = service._calculate_seat_grid(seat_num, capacity)
        grid_display[grid['row']][grid['col']][grid['position']] = {
            'seat': seat_num,
            'subject': subject,
            'name': name
        }
        print(f"  {name:8s} - Seat {seat_num:2d} - Row {grid['row']}, Col {grid['col']}, {grid['position']:5s}")

    print()

    print("Room Layout (Front of Room)")
    print("=" * 80)
    print()

    col_width = 18

    print("     ", end="")
    for col in range(4):
        print(f"Col {col}".center(col_width), end="")
    print()
    print("     " + "-" * (col_width * 4))

    for row in range(4):
        print(f"Row {row}|", end="")

        for col in range(4):
            left_info = grid_display[row][col]['left']
            right_info = grid_display[row][col]['right']

            if left_info:
                left_str = f"[{left_info['seat']:2d}:{left_info['name'][:4]}]"
            else:
                left_str = "[  :    ]"

            if right_info:
                right_str = f"[{right_info['seat']:2d}:{right_info['name'][:4]}]"
            else:
                right_str = "[  :    ]"

            print(f" {left_str}{right_str} ", end="")

        print()

    print()
    print("Legend: [Seat#:Name] - Each pair is a bench")
    print()

    print("\n" + "=" * 80)
    print("Placement Rules Demonstration for Next Math Student")
    print("=" * 80 + "\n")

    blocked_beside = []
    blocked_across = []
    allowed = []

    for seat_num in range(1, capacity + 1):
        if seat_num in seat_subjects:
            continue

        can_place = service._can_place_subject_at_seat(
            seat_subjects, seat_num, "Math", capacity
        )

        grid = service._calculate_seat_grid(seat_num, capacity)

        if not can_place:
            blocked = False
            for existing_seat, existing_subj in seat_subjects.items():
                if existing_subj == "Math":
                    existing_grid = service._calculate_seat_grid(existing_seat, capacity)

                    if grid['bench_num'] == existing_grid['bench_num']:
                        blocked_beside.append((seat_num, existing_seat, grid))
                        blocked = True
                        break
                    elif grid['col'] == existing_grid['col']:
                        blocked_across.append((seat_num, existing_seat, grid))
                        blocked = True
                        break
        else:
            allowed.append((seat_num, grid))

    print(f"❌ BLOCKED - Beside (same bench): {len(blocked_beside)} seats")
    for seat_num, existing_seat, grid in blocked_beside[:5]:
        print(f"   Seat {seat_num:2d} (Row {grid['row']}, Col {grid['col']}, {grid['position']:5s}) "
              f"- blocked by Seat {existing_seat}")
    if len(blocked_beside) > 5:
        print(f"   ... and {len(blocked_beside) - 5} more")

    print()
    print(f"❌ BLOCKED - Across (same column): {len(blocked_across)} seats")
    for seat_num, existing_seat, grid in blocked_across[:5]:
        print(f"   Seat {seat_num:2d} (Row {grid['row']}, Col {grid['col']}, {grid['position']:5s}) "
              f"- blocked by Seat {existing_seat}")
    if len(blocked_across) > 5:
        print(f"   ... and {len(blocked_across) - 5} more")

    print()
    print(f"✅ ALLOWED - Different columns: {len(allowed)} seats")
    for seat_num, grid in allowed[:8]:
        print(f"   Seat {seat_num:2d} (Row {grid['row']}, Col {grid['col']}, {grid['position']:5s})")
    if len(allowed) > 8:
        print(f"   ... and {len(allowed) - 8} more")

    print()

    print("=" * 80)
    print("Summary:")
    print(f"  • Total seats: {capacity}")
    print(f"  • Occupied: {len(seat_subjects)}")
    print(f"  • Available: {capacity - len(seat_subjects)}")
    print(f"  • Blocked for Math students: {len(blocked_beside) + len(blocked_across)}")
    print(f"  • Allowed for Math students: {len(allowed)}")
    print(f"  • Blocked percentage: {(len(blocked_beside) + len(blocked_across)) / (capacity - len(seat_subjects)) * 100:.1f}%")
    print("=" * 80 + "\n")

    print("Grid Visualization with Blocking:")
    print("=" * 80)
    print()
    print("Legend:")
    print("  [XX:Name] - Occupied by Math student")
    print("  [❌]       - Blocked for Math students")
    print("  [✓]       - Available for Math students")
    print()

    print("     ", end="")
    for col in range(4):
        print(f"Col {col}".center(col_width), end="")
    print()
    print("     " + "-" * (col_width * 4))

    blocking_map = {}
    for seat_num, existing_seat, grid in blocked_beside + blocked_across:
        blocking_map[seat_num] = '❌'
    for seat_num, grid in allowed:
        blocking_map[seat_num] = '✓'

    for row in range(4):
        print(f"Row {row}|", end="")

        for col in range(4):
            bench_num = row * 4 + col
            left_seat = bench_num * 2 + 1
            right_seat = bench_num * 2 + 2

            if left_seat in seat_subjects:
                left_info = grid_display[row][col]['left']
                left_str = f"[{left_seat:2d}:{left_info['name'][:4]}]"
            elif left_seat in blocking_map:
                left_str = f"[{blocking_map[left_seat]:^7s}]"
            else:
                left_str = "[       ]"

            if right_seat in seat_subjects:
                right_info = grid_display[row][col]['right']
                right_str = f"[{right_seat:2d}:{right_info['name'][:4]}]"
            elif right_seat in blocking_map:
                right_str = f"[{blocking_map[right_seat]:^7s}]"
            else:
                right_str = "[       ]"

            print(f" {left_str}{right_str} ", end="")

        print()

    print()
    print("=" * 80 + "\n")


if __name__ == "__main__":
    visualize_room_grid()
