"""
Advanced seat allocation service with intelligent anti-copying algorithms
"""
import random
import math
from collections import defaultdict, Counter

class AllocationService:
    def __init__(self):
        self.MIN_DISTANCE = 2  # Minimum seats between same subjects
        self.MAX_ATTEMPTS = 1000  # Maximum attempts to find valid placement
        self.PREFERRED_DISTANCE = 3  # Preferred distance for better separation
    
    def allocate_seats(self, students, rooms, strategy='mixed'):
        """
        Main allocation method
        
        Args:
            students: List of student documents
            rooms: List of room documents
            strategy: 'mixed', 'separated', or 'optimal_packing'
        
        Returns:
            Dict with allocations and summary
        """
        if strategy == 'mixed':
            return self._allocate_mixed_strategy(students, rooms)
        elif strategy == 'separated':
            return self._allocate_separated_strategy(students, rooms)
        elif strategy == 'optimal_packing':
            return self._allocate_optimal_packing_strategy(students, rooms)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _allocate_mixed_strategy(self, students, rooms):
        students_by_subject = defaultdict(list)
        for student in students:
            # Handle both single and multi-subject students
            student_subjects = student.get('subjects', [])
            if not student_subjects and student.get('subject'):
                student_subjects = [student['subject']]
            
            # For multi-subject students, use the first subject for allocation
            primary_subject = student_subjects[0] if student_subjects else 'Unknown'
            students_by_subject[primary_subject].append(student)
        
        # Enhanced shuffling with seeded randomness for reproducible but random results
        for subject in students_by_subject:
            random.shuffle(students_by_subject[subject])
        
        # Calculate optimal distribution ratios
        total_students = len(students)
        total_capacity = sum(room['capacity'] for room in rooms)
        
        # Sort subjects by count (balanced approach - not just largest first)
        sorted_subjects = self._calculate_optimal_subject_order(students_by_subject)
        
        allocations = []
        total_allocated = 0
        
        # Sort rooms by strategic importance (capacity and layout considerations)
        sorted_rooms = self._sort_rooms_strategically(rooms)
        
        for room in sorted_rooms:
            if total_allocated >= total_students:
                break
                
            remaining_students = total_students - total_allocated
            if remaining_students == 0:
                break
            
            room_allocation = self._allocate_room_advanced(
                room, students_by_subject, sorted_subjects, remaining_students
            )
            
            if room_allocation['students']:
                allocations.append(room_allocation)
                total_allocated += len(room_allocation['students'])
        
        # Post-process for optimization
        self._optimize_allocations(allocations)
        
        # Generate comprehensive summary
        summary = self._generate_enhanced_summary(allocations, students)
        
        return {
            'allocations': allocations,
            'summary': summary,
            'strategy': 'mixed_advanced'
        }
    
    def _allocate_room_advanced(self, room, students_by_subject, sorted_subjects, remaining_students):
        """Advanced room allocation with intelligent seating patterns and optimal subject distribution"""
        capacity = room['capacity']
        allocated_students = []
        
        # Create a 2D grid representation for better spatial awareness
        # Improved grid calculation for optimal seating arrangement
        rows = max(1, int(math.sqrt(capacity)))
        cols = max(1, math.ceil(capacity / rows))
        seat_grid = {}
        seat_subjects = {}
        
        # Generate optimal seating pattern based on room layout
        seat_positions = self._generate_optimal_seat_positions(capacity, rows, cols)
        
        # Enhanced quota calculation with better subject balancing
        subject_quotas = self._calculate_enhanced_room_quotas(
            students_by_subject, capacity, remaining_students
        )
        
        # Advanced allocation using multiple passes for better distribution
        allocated_count = 0
        max_attempts = min(self.MAX_ATTEMPTS, capacity * 3)  # More efficient attempt limit
        
        # Pass 1: Strategic allocation with maximum separation
        allocated_count = self._allocate_with_strategy(
            students_by_subject, sorted_subjects, subject_quotas, 
            seat_positions, seat_subjects, allocated_students, 
            capacity, self.PREFERRED_DISTANCE, "preferred"
        )
        
        # Pass 2: Fill remaining seats with minimum distance requirement
        if allocated_count < capacity:
            allocated_count = self._allocate_with_strategy(
                students_by_subject, sorted_subjects, subject_quotas, 
                seat_positions, seat_subjects, allocated_students, 
                capacity, self.MIN_DISTANCE, "minimum"
            )
        
        # Pass 3: Emergency fill with adaptive distance
        if allocated_count < capacity:
            self._emergency_fill_seats(
                students_by_subject, sorted_subjects, 
                seat_positions, seat_subjects, allocated_students, capacity
            )
        
        # Sort by seat number for organized output
        allocated_students.sort(key=lambda x: x['seat_number'])
        
        # Calculate enhanced subject breakdown with distribution metrics
        subject_breakdown = self._calculate_enhanced_breakdown(allocated_students, seat_subjects)
        
        return {
            'room': room,
            'students': allocated_students,
            'subject_breakdown': subject_breakdown,
            'distribution_score': self._calculate_distribution_score(seat_subjects, capacity),
            'separation_quality': self._calculate_separation_quality(seat_subjects, rows, cols)
        }
    
    def _allocate_separated_strategy(self, students, rooms):
        """
        Enhanced separated strategy: Intelligently distribute subjects across rooms with optimal spacing
        """
        # Group students by subject with enhanced handling
        students_by_subject = defaultdict(list)
        for student in students:
            student_subjects = student.get('subjects', [])
            if not student_subjects and student.get('subject'):
                student_subjects = [student['subject']]
            
            primary_subject = student_subjects[0] if student_subjects else 'Unknown'
            students_by_subject[primary_subject].append(student)
        
        # Enhanced shuffling for better distribution
        for subject in students_by_subject:
            random.shuffle(students_by_subject[subject])
        
        # Calculate optimal room distribution
        room_distribution = self._calculate_optimal_room_distribution(students_by_subject, rooms)
        
        allocations = []
        
        # Process each room with its assigned subjects
        for room_id, room_data in room_distribution.items():
            room = room_data['room']
            assigned_subjects = room_data['subjects']
            
            if not assigned_subjects:
                continue
            
            # Allocate students within this room using advanced algorithm
            room_allocation = self._allocate_separated_room(
                room, assigned_subjects, students_by_subject
            )
            
            if room_allocation['students']:
                allocations.append(room_allocation)
        
        # Generate enhanced summary
        summary = self._generate_enhanced_summary(allocations, students)
        
        return {
            'allocations': allocations,
            'summary': summary,
            'strategy': 'separated_advanced'
        }
    
    def _allocate_optimal_packing_strategy(self, students, rooms):
        """
        Optimal packing strategy: Use minimum number of rooms while maintaining shuffled distribution
        
        This strategy maximizes room utilization by:
        1. Sorting rooms by capacity (largest first)
        2. Shuffling students thoroughly for random distribution
        3. Packing students as tightly as possible while maintaining anti-copying measures
        4. Only using additional rooms when necessary
        """
        # Thoroughly shuffle all students for maximum randomization
        shuffled_students = students.copy()
        random.shuffle(shuffled_students)
        
        # Group shuffled students by subject for anti-copying measures
        students_by_subject = defaultdict(list)
        for student in shuffled_students:
            # Handle both single and multi-subject students
            student_subjects = student.get('subjects', [])
            if not student_subjects and student.get('subject'):
                student_subjects = [student['subject']]
            
            primary_subject = student_subjects[0] if student_subjects else 'Unknown'
            students_by_subject[primary_subject].append(student)
        
        # Sort rooms by capacity (largest first) to minimize room usage
        sorted_rooms = sorted(rooms, key=lambda r: r['capacity'], reverse=True)
        
        allocations = []
        total_allocated = 0
        total_students = len(students)
        
        # Create a mixed pool of students for optimal packing
        student_pool = self._create_optimal_student_pool(students_by_subject)
        
        for room in sorted_rooms:
            if total_allocated >= total_students:
                break
                
            remaining_students = total_students - total_allocated
            if remaining_students == 0:
                break
            
            # Determine how many students to allocate to this room
            room_capacity = room['capacity']
            students_to_allocate = min(room_capacity, remaining_students)
            
            # Allocate students to this room with optimal packing
            room_allocation = self._allocate_room_optimal_packing(
                room, student_pool, students_to_allocate
            )
            
            if room_allocation['students']:
                allocations.append(room_allocation)
                total_allocated += len(room_allocation['students'])
                
                # Remove allocated students from the pool
                allocated_student_objects = [alloc['student'] for alloc in room_allocation['students']]
                student_pool = [s for s in student_pool if s not in allocated_student_objects]
        
        # Generate comprehensive summary
        summary = self._generate_enhanced_summary(allocations, students)
        summary['rooms_saved'] = len(rooms) - len(allocations)
        summary['utilization_efficiency'] = self._calculate_utilization_efficiency(allocations, rooms)
        
        return {
            'allocations': allocations,
            'summary': summary,
            'strategy': 'optimal_packing'
        }
    
    def _create_optimal_student_pool(self, students_by_subject):
        """
        Create an optimally shuffled pool of students that ensures good distribution
        while maintaining randomness
        """
        student_pool = []
        subjects = list(students_by_subject.keys())
        
        # Create a round-robin distribution to ensure no subject clusters
        max_students_per_subject = max(len(students) for students in students_by_subject.values())
        
        for i in range(max_students_per_subject):
            # Shuffle subjects order for each round
            shuffled_subjects = subjects.copy()
            random.shuffle(shuffled_subjects)
            
            for subject in shuffled_subjects:
                if i < len(students_by_subject[subject]):
                    student_pool.append(students_by_subject[subject][i])
        
        # Final shuffle to add more randomness
        random.shuffle(student_pool)
        return student_pool
    
    def _allocate_room_optimal_packing(self, room, student_pool, students_to_allocate):
        """
        Allocate students to a room using optimal packing with anti-copying measures
        """
        capacity = room['capacity']
        allocated_students = []
        seat_subjects = {}
        
        # Create seat positions for optimal distribution
        rows = max(1, int(math.sqrt(capacity)))
        cols = max(1, math.ceil(capacity / rows))
        seat_positions = self._generate_optimal_seat_positions(capacity, rows, cols)
        
        # Take students from the pool and allocate them optimally
        students_to_place = student_pool[:students_to_allocate]
        
        for i, student in enumerate(students_to_place):
            if i >= capacity:
                break
                
            # Get student's primary subject
            student_subjects = student.get('subjects', [])
            if not student_subjects and student.get('subject'):
                student_subjects = [student['subject']]
            primary_subject = student_subjects[0] if student_subjects else 'Unknown'
            
            # Find optimal seat position
            best_seat = self._find_optimal_packing_seat(
                seat_positions, seat_subjects, primary_subject, i + 1
            )
            
            if best_seat:
                allocated_students.append({
                    'seat_number': best_seat,
                    'student': student
                })
                seat_subjects[best_seat] = primary_subject
        
        # Sort by seat number for organized output
        allocated_students.sort(key=lambda x: x['seat_number'])
        
        # Calculate subject breakdown
        subject_breakdown = self._calculate_enhanced_breakdown(allocated_students, seat_subjects)
        
        return {
            'room': room,
            'students': allocated_students,
            'subject_breakdown': subject_breakdown,
            'utilization_rate': len(allocated_students) / capacity * 100,
            'packing_efficiency': self._calculate_packing_efficiency(allocated_students, capacity)
        }
    
    def _find_optimal_packing_seat(self, seat_positions, seat_subjects, subject, priority):
        """
        Find the optimal seat for packing strategy that balances density with anti-copying
        """
        available_seats = [pos for pos in seat_positions if pos['seat'] not in seat_subjects]
        
        if not available_seats:
            return None
        
        # For optimal packing, prioritize:
        # 1. Fill seats sequentially for maximum density
        # 2. But maintain minimum distance for same subjects
        
        best_seat = None
        best_score = -1
        
        for seat_pos in available_seats:
            seat_num = seat_pos['seat']
            
            # Calculate anti-copying score
            min_distance = self._calculate_min_distance_to_subject(
                seat_subjects, seat_num, subject, len(seat_positions)
            )
            
            # Packing score: prefer lower seat numbers for density
            packing_score = len(seat_positions) - seat_num
            
            # Combined score
            if min_distance >= self.MIN_DISTANCE:
                # Good separation, prioritize packing
                score = packing_score * 10 + min_distance
            else:
                # Poor separation, heavily penalize
                score = min_distance - 100
            
            if score > best_score:
                best_score = score
                best_seat = seat_num
        
        # If no seat meets minimum distance, find the best available compromise
        if best_seat is None:
            # Emergency allocation: find seat with maximum possible distance
            for seat_pos in available_seats:
                seat_num = seat_pos['seat']
                min_distance = self._calculate_min_distance_to_subject(
                    seat_subjects, seat_num, subject, len(seat_positions)
                )
                
                if min_distance > best_score:
                    best_score = min_distance
                    best_seat = seat_num
        
        return best_seat or (available_seats[0]['seat'] if available_seats else None)
    
    def _calculate_utilization_efficiency(self, allocations, rooms):
        """Calculate overall room utilization efficiency"""
        if not allocations:
            return 0
            
        total_capacity = sum(room['capacity'] for room in rooms)
        total_allocated = sum(len(alloc['students']) for alloc in allocations)
        used_capacity = sum(alloc['room']['capacity'] for alloc in allocations)
        
        # Efficiency combines allocation rate with room usage optimization
        allocation_efficiency = (total_allocated / total_capacity) * 100 if total_capacity > 0 else 0
        room_usage_efficiency = (total_allocated / used_capacity) * 100 if used_capacity > 0 else 0
        
        return round((allocation_efficiency + room_usage_efficiency) / 2, 2)
    
    def _calculate_packing_efficiency(self, allocated_students, capacity):
        """Calculate how efficiently the room is packed"""
        if capacity == 0:
            return 0
        return round((len(allocated_students) / capacity) * 100, 2)
    
    def _calculate_optimal_room_distribution(self, students_by_subject, rooms):
        """Calculate optimal distribution of subjects across rooms"""
        room_distribution = {}
        
        # Initialize room data
        for room in rooms:
            room_distribution[room['_id']] = {
                'room': room,
                'subjects': {},
                'capacity': room['capacity'],
                'assigned_count': 0
            }
        
        # Sort subjects by count for better distribution
        sorted_subjects = sorted(
            students_by_subject.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        room_ids = list(room_distribution.keys())
        
        # Distribute subjects across rooms using round-robin with capacity awareness
        for subject, students in sorted_subjects:
            students_count = len(students)
            
            if students_count <= len(rooms):
                # Small subject group: distribute one per room
                for i, student in enumerate(students):
                    room_idx = i % len(room_ids)
                    room_id = room_ids[room_idx]
                    
                    if room_distribution[room_id]['assigned_count'] < room_distribution[room_id]['capacity']:
                        if subject not in room_distribution[room_id]['subjects']:
                            room_distribution[room_id]['subjects'][subject] = []
                        room_distribution[room_id]['subjects'][subject].append(student)
                        room_distribution[room_id]['assigned_count'] += 1
            else:
                # Large subject group: distribute proportionally
                students_per_room = max(1, students_count // len(rooms))
                remaining_students = students[:]
                
                for room_id in room_ids:
                    room_data = room_distribution[room_id]
                    available_capacity = room_data['capacity'] - room_data['assigned_count']
                    
                    take_count = min(students_per_room, available_capacity, len(remaining_students))
                    
                    if take_count > 0:
                        if subject not in room_data['subjects']:
                            room_data['subjects'][subject] = []
                        
                        room_data['subjects'][subject].extend(remaining_students[:take_count])
                        room_data['assigned_count'] += take_count
                        remaining_students = remaining_students[take_count:]
                
                # Distribute any remaining students
                room_idx = 0
                while remaining_students and room_idx < len(room_ids):
                    room_id = room_ids[room_idx]
                    room_data = room_distribution[room_id]
                    
                    if room_data['assigned_count'] < room_data['capacity']:
                        if subject not in room_data['subjects']:
                            room_data['subjects'][subject] = []
                        
                        room_data['subjects'][subject].append(remaining_students.pop(0))
                        room_data['assigned_count'] += 1
                    
                    room_idx = (room_idx + 1) % len(room_ids)
        
        return room_distribution
    
    def _allocate_separated_room(self, room, assigned_subjects, students_by_subject):
        """Allocate students within a single room for separated strategy"""
        capacity = room['capacity']
        allocated_students = []
        seat_subjects = {}
        
        # Create a queue of all students to assign
        student_queue = []
        for subject, students in assigned_subjects.items():
            for student in students:
                student_queue.append((student, subject))
        
        # Shuffle for randomization while maintaining subject separation
        random.shuffle(student_queue)
        
        # Generate seat positions with optimal spacing
        seat_positions = self._generate_optimal_seat_positions(capacity, 
                                                             int(math.sqrt(capacity)) + 1,
                                                             int(capacity / (int(math.sqrt(capacity)) + 1)) + 1)
        
        # Allocate with maximum separation
        for student, subject in student_queue:
            if len(allocated_students) >= capacity:
                break
            
            # Find best seat with maximum separation from same subject
            best_seat = self._find_best_seat_position(
                seat_positions, seat_subjects, subject, capacity,
                prefer_distance=self.PREFERRED_DISTANCE
            )
            
            if best_seat:
                allocated_students.append({
                    'seat_number': best_seat,
                    'student': student
                })
                seat_subjects[best_seat] = subject
        
        # Sort by seat number
        allocated_students.sort(key=lambda x: x['seat_number'])
        
        # Calculate subject breakdown
        subject_breakdown = self._calculate_enhanced_breakdown(allocated_students, seat_subjects)
        
        return {
            'room': room,
            'students': allocated_students,
            'subject_breakdown': subject_breakdown,
            'distribution_score': self._calculate_distribution_score(seat_subjects, capacity)
        }
    
    def _calculate_optimal_subject_order(self, students_by_subject):
        """Calculate optimal subject ordering for better distribution"""
        subjects = list(students_by_subject.keys())
        subject_counts = {s: len(students_by_subject[s]) for s in subjects}
        
        # Sort by a combination of count and spread factor
        return sorted(subjects, key=lambda s: (
            -subject_counts[s],  # Higher count first
            hash(s) % 100  # Add deterministic randomness for equal counts
        ))
    
    def _sort_rooms_strategically(self, rooms):
        """Sort rooms for optimal allocation strategy"""
        return sorted(rooms, key=lambda r: (
            -r['capacity'],  # Larger rooms first
            r.get('name', ''),  # Alphabetical for consistency
        ))
    
    def _generate_optimal_seat_positions(self, capacity, rows, cols):
        """Generate seat positions optimized for subject separation"""
        positions = []
        
        # Create a pattern that maximizes distance between similar positions
        for seat in range(1, capacity + 1):
            row = (seat - 1) // cols
            col = (seat - 1) % cols
            positions.append({
                'seat': seat,
                'row': row,
                'col': col,
                'position_score': self._calculate_position_score(row, col, rows, cols)
            })
        
        return sorted(positions, key=lambda p: p['position_score'])
    
    def _calculate_position_score(self, row, col, total_rows, total_cols):
        """Calculate position desirability score"""
        # Prefer positions that are more distributed
        center_row = total_rows / 2
        center_col = total_cols / 2
        
        # Distance from center (prefer corners and edges for better separation)
        distance_from_center = math.sqrt((row - center_row)**2 + (col - center_col)**2)
        
        # Add checkerboard pattern bonus
        checkerboard_bonus = 10 if (row + col) % 2 == 0 else 0
        
        return distance_from_center + checkerboard_bonus
    
    def _calculate_room_quotas(self, students_by_subject, room_capacity, remaining_students):
        """Calculate how many students of each subject should be in this room"""
        quotas = {}
        total_students = sum(len(students) for students in students_by_subject.values())
        
        if total_students == 0:
            return quotas
        
        # Calculate proportional quotas
        room_allocation = min(room_capacity, remaining_students)
        
        for subject, students in students_by_subject.items():
            if students:  # Only consider subjects with remaining students
                proportion = len(students) / total_students
                quota = max(1, int(room_allocation * proportion))
                quotas[subject] = min(quota, len(students))
        
        return quotas
    
    def _find_best_seat_position(self, seat_positions, seat_subjects, subject, capacity, prefer_distance):
        """Find the best available seat position for a subject"""
        available_seats = [pos for pos in seat_positions 
                          if pos['seat'] not in seat_subjects]
        
        if not available_seats:
            return None
        
        # Score each available seat based on separation from same subjects
        best_seat = None
        best_score = -1
        
        for seat_pos in available_seats:
            seat_num = seat_pos['seat']
            
            # Calculate separation score
            min_distance = self._calculate_min_distance_to_subject(
                seat_subjects, seat_num, subject, capacity
            )
            
            if min_distance >= prefer_distance:
                # This seat meets the preferred distance requirement
                score = min_distance + seat_pos['position_score']
                if score > best_score:
                    best_score = score
                    best_seat = seat_num
        
        # If no seat meets preferred distance, try minimum distance
        if best_seat is None and prefer_distance > self.MIN_DISTANCE:
            return self._find_best_seat_position(
                seat_positions, seat_subjects, subject, capacity, self.MIN_DISTANCE
            )
        
        # If still no seat, just return the first available one
        if best_seat is None and prefer_distance == self.MIN_DISTANCE:
            for seat_pos in available_seats:
                seat_num = seat_pos['seat']
                if self._can_place_subject_at_seat(seat_subjects, seat_num, subject, capacity):
                    return seat_num
        
        return best_seat
    
    def _calculate_min_distance_to_subject(self, seat_subjects, seat_num, subject, capacity):
        """Calculate minimum distance to nearest seat with same subject"""
        min_distance = capacity  # Max possible distance
        
        for existing_seat, existing_subject in seat_subjects.items():
            if existing_subject == subject:
                distance = abs(existing_seat - seat_num)
                min_distance = min(min_distance, distance)
        
        return min_distance
    
    def _can_place_subject_at_seat(self, seat_subjects, seat_num, subject, capacity):
        """Enhanced check if a subject can be placed at a specific seat"""
        # Check minimum distance requirement
        return self._calculate_min_distance_to_subject(
            seat_subjects, seat_num, subject, capacity
        ) >= self.MIN_DISTANCE
    
    def _calculate_enhanced_breakdown(self, allocated_students, seat_subjects):
        """Calculate enhanced subject breakdown with distribution metrics"""
        breakdown = Counter()
        
        for allocation in allocated_students:
            student = allocation['student']
            student_subjects = student.get('subjects', [])
            if not student_subjects and student.get('subject'):
                student_subjects = [student['subject']]
            primary_subject = student_subjects[0] if student_subjects else 'Unknown'
            breakdown[primary_subject] += 1
        
        return dict(breakdown)
    
    def _calculate_distribution_score(self, seat_subjects, capacity):
        """Calculate how well subjects are distributed (higher is better)"""
        if not seat_subjects:
            return 0
        
        # Calculate average distance between same subjects
        subject_distances = defaultdict(list)
        
        for seat1, subject1 in seat_subjects.items():
            for seat2, subject2 in seat_subjects.items():
                if seat1 < seat2 and subject1 == subject2:
                    distance = abs(seat2 - seat1)
                    subject_distances[subject1].append(distance)
        
        # Calculate average minimum distance
        total_score = 0
        for subject, distances in subject_distances.items():
            if distances:
                avg_distance = sum(distances) / len(distances)
                total_score += avg_distance
        
        return round(total_score / len(subject_distances) if subject_distances else capacity, 2)
    
    def _optimize_allocations(self, allocations):
        """Post-process allocations for final optimization"""
        # This could implement swap operations to improve distribution
        # For now, just ensure consistent formatting
        for allocation in allocations:
            allocation['students'].sort(key=lambda x: x['seat_number'])
    
    def _calculate_enhanced_room_quotas(self, students_by_subject, room_capacity, remaining_students):
        quotas = {}
        total_students = sum(len(students) for students in students_by_subject.values())
        if total_students == 0:
            return quotas
        room_allocation = min(room_capacity, remaining_students)
        
        subjects_with_students = {s: students for s, students in students_by_subject.items() if students}
        min_per_subject = max(1, room_allocation // len(subjects_with_students)) if subjects_with_students else 0
        
        for subject, students in subjects_with_students.items():
            base_quota = min(min_per_subject, len(students))
            quotas[subject] = base_quota
        
        allocated_so_far = sum(quotas.values())
        remaining_capacity = room_allocation - allocated_so_far
        
        if remaining_capacity > 0:
            for subject, students in sorted(subjects_with_students.items(), 
                                          key=lambda x: len(x[1]), reverse=True):
                if remaining_capacity <= 0:
                    break
                
                current_quota = quotas[subject]
                max_additional = min(remaining_capacity, len(students) - current_quota)
                
                if max_additional > 0:
                    additional = min(max_additional, max(1, remaining_capacity // 2))
                    quotas[subject] += additional
                    remaining_capacity -= additional
        
        return quotas
    
    def _allocate_with_strategy(self, students_by_subject, sorted_subjects, subject_quotas, 
                               seat_positions, seat_subjects, allocated_students, 
                               capacity, min_distance, strategy_name):
        """Allocate students with specific distance strategy"""
        allocated_count = len(allocated_students)
        max_iterations = min(capacity * 2, 200)  # Prevent infinite loops
        
        for iteration in range(max_iterations):
            if allocated_count >= capacity:
                break

            made_allocation = False
            
            for subject in sorted_subjects:
                if not students_by_subject[subject] or subject_quotas.get(subject, 0) <= 0:
                    continue
                
                best_seat = self._find_best_seat_position(
                    seat_positions, seat_subjects, subject, capacity, min_distance
                )
                
                if best_seat:
                    student = students_by_subject[subject].pop(0)
                    allocated_students.append({
                        'seat_number': best_seat,
                        'student': student
                    })
                    seat_subjects[best_seat] = subject
                    subject_quotas[subject] -= 1
                    allocated_count += 1
                    made_allocation = True
                    
                    if allocated_count >= capacity:
                        break
            
            # If no allocations were made in this iteration, break to avoid infinite loop
            if not made_allocation:
                break
        
        return allocated_count
    
    def _emergency_fill_seats(self, students_by_subject, sorted_subjects, 
                             seat_positions, seat_subjects, allocated_students, capacity):
        """Emergency fill remaining seats with any available students"""
        allocated_count = len(allocated_students)
        
        # Get all available seats
        available_seats = [pos['seat'] for pos in seat_positions 
                          if pos['seat'] not in seat_subjects]
        
        # Get all remaining students
        all_remaining_students = []
        for subject in sorted_subjects:
            for student in students_by_subject[subject]:
                all_remaining_students.append((student, subject))
        
        # Fill available seats
        for i, (student, subject) in enumerate(all_remaining_students):
            if i >= len(available_seats) or allocated_count >= capacity:
                break
                
            seat_num = available_seats[i]
            allocated_students.append({
                'seat_number': seat_num,
                'student': student
            })
            seat_subjects[seat_num] = subject
            allocated_count += 1
        
        # Remove allocated students from the subject lists
        allocated_subjects = {}
        for alloc in allocated_students[-len(all_remaining_students):]:
            student = alloc['student']
            student_subjects = student.get('subjects', [])
            if not student_subjects and student.get('subject'):
                student_subjects = [student['subject']]
            primary_subject = student_subjects[0] if student_subjects else 'Unknown'
            
            if primary_subject not in allocated_subjects:
                allocated_subjects[primary_subject] = []
            allocated_subjects[primary_subject].append(student)
        
        # Remove from original lists
        for subject, allocated_students_list in allocated_subjects.items():
            if subject in students_by_subject:
                for student in allocated_students_list:
                    if student in students_by_subject[subject]:
                        students_by_subject[subject].remove(student)
    
    def _calculate_separation_quality(self, seat_subjects, rows, cols):
        """Calculate how well subjects are separated spatially"""
        if not seat_subjects:
            return 0
        
        total_score = 0
        total_pairs = 0
        
        for seat1, subject1 in seat_subjects.items():
            for seat2, subject2 in seat_subjects.items():
                if seat1 < seat2:  # Avoid double counting
                    total_pairs += 1
                    
                    # Calculate spatial distance
                    row1, col1 = divmod(seat1 - 1, cols)
                    row2, col2 = divmod(seat2 - 1, cols)
                    spatial_distance = math.sqrt((row2 - row1)**2 + (col2 - col1)**2)
                    
                    # Same subject penalty
                    if subject1 == subject2:
                        if spatial_distance >= 2:
                            total_score += spatial_distance * 0.8  # Good separation
                        else:
                            total_score -= 2  # Penalty for close same subjects
                    else:
                        total_score += min(spatial_distance, 3)  # Bonus for different subjects
        
        return round(total_score / max(total_pairs, 1), 2)
    
    def _generate_enhanced_summary(self, allocations, students):
        """Generate enhanced allocation summary with quality metrics"""
        summary = self._generate_summary(allocations, students)
        
        # Add distribution quality metrics
        total_distribution_score = sum(
            alloc.get('distribution_score', 0) for alloc in allocations
        )
        avg_distribution_score = (
            total_distribution_score / len(allocations) if allocations else 0
        )
        
        # Add separation quality metrics
        total_separation_score = sum(
            alloc.get('separation_quality', 0) for alloc in allocations
        )
        avg_separation_score = (
            total_separation_score / len(allocations) if allocations else 0
        )
        
        summary.update({
            'average_distribution_score': round(avg_distribution_score, 2),
            'average_separation_score': round(avg_separation_score, 2),
            'quality_rating': self._calculate_quality_rating(summary, avg_distribution_score, avg_separation_score),
            'algorithm_version': 'advanced_v3.0'
        })
        
        return summary
    
    def _calculate_quality_rating(self, summary, distribution_score, separation_score=0):
        """Calculate overall allocation quality rating"""
        allocation_pct = summary.get('allocation_percentage', 0)
        
        # Combine distribution and separation scores
        combined_score = (distribution_score + separation_score) / 2
        
        if allocation_pct >= 95 and combined_score >= 3:
            return 'Excellent'
        elif allocation_pct >= 90 and combined_score >= 2:
            return 'Very Good'
        elif allocation_pct >= 85 and combined_score >= 1.5:
            return 'Good'
        elif allocation_pct >= 70 and combined_score >= 1:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def _generate_summary(self, allocations, students):
        """Generate allocation summary statistics"""
        total_allocated = sum(len(alloc['students']) for alloc in allocations)
        total_students = len(students)
        rooms_used = len(allocations)
        
        # Subject distribution
        subject_counts = defaultdict(int)
        for alloc in allocations:
            for subject, count in alloc['subject_breakdown'].items():
                subject_counts[subject] += count
        
        return {
            'total_students': total_students,
            'total_allocated': total_allocated,
            'total_unallocated': total_students - total_allocated,
            'rooms_used': rooms_used,
            'subject_distribution': dict(subject_counts),
            'allocation_percentage': round((total_allocated / total_students) * 100, 2) if total_students > 0 else 0
        }
