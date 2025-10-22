"""
Enhanced PDF report generation service with improved subject formatting
"""
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class PDFService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='RoomHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            textColor=colors.darkgreen
        ))
    
    def generate_allocation_report(self, allocation):
        """Generate PDF report for single allocation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Build the document
        story = []
        
        # Title
        title = Paragraph("Exam Seat Allocation Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Allocation info
        info_data = [
            ['Generated On:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Strategy:', allocation.get('strategy', 'N/A').title()],
            ['Subject Filter:', allocation.get('subject_filter', 'All Subjects') or 'All Subjects']
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Enhanced Summary with quality metrics
        summary = allocation.get('allocation_summary', {})
        summary_header = Paragraph("Allocation Summary", self.styles['SectionHeader'])
        story.append(summary_header)
        
        summary_data = [
            ['Total Students:', str(summary.get('total_students', 0))],
            ['Students Allocated:', str(summary.get('total_allocated', 0))],
            ['Students Unallocated:', str(summary.get('total_unallocated', 0))],
            ['Rooms Used:', str(summary.get('rooms_used', 0))],
            ['Allocation Rate:', f"{summary.get('allocation_percentage', 0)}%"],
            ['Quality Rating:', summary.get('quality_rating', 'N/A')],
            ['Distribution Score:', str(summary.get('average_distribution_score', 'N/A'))],
            ['Separation Score:', str(summary.get('average_separation_score', 'N/A'))]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Room allocations
        allocations = allocation.get('allocations', [])
        if allocations:
            rooms_header = Paragraph("Room-wise Seat Allocation", self.styles['SectionHeader'])
            story.append(rooms_header)
            
            for room_alloc in allocations:
                self._add_room_allocation_to_story(story, room_alloc)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_multi_exam_report(self, allocation):
        """Generate PDF report for multi-exam allocation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        title = Paragraph("Multi-Exam Seat Allocation Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Session info
        session_info = allocation.get('session_info', {})
        summary = allocation.get('allocation_summary', {})
        report_data = summary.get('report_data', {})
        
        info_data = [
            ['Generated On:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Session Name:', session_info.get('session_name', 'Multi-Exam Session')],
            ['Created By:', session_info.get('created_by', 'System Administrator')],
            ['Strategy:', allocation.get('strategy', 'N/A').title()]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Exam details
        if report_data.get('exams'):
            exam_header = Paragraph("Exam Details", self.styles['SectionHeader'])
            story.append(exam_header)
            
            exam_table_data = [['Exam Name', 'Subject', 'Duration (min)', 'Students', 'Allocated']]
            
            for exam in report_data['exams']:
                exam_table_data.append([
                    exam['exam_name'],
                    exam['subject'],
                    str(exam['duration']),
                    str(exam['total_students']),
                    str(exam['allocated_students'])
                ])
            
            exam_table = Table(exam_table_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
            exam_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(exam_table)
            story.append(Spacer(1, 20))
        
        # Summary
        summary_header = Paragraph("Allocation Summary", self.styles['SectionHeader'])
        story.append(summary_header)
        
        summary_data = [
            ['Total Students:', str(summary.get('total_students', 0))],
            ['Students Allocated:', str(summary.get('total_allocated', 0))],
            ['Students Unallocated:', str(summary.get('total_unallocated', 0))],
            ['Rooms Used:', str(summary.get('rooms_used', 0))],
            ['Allocation Rate:', f"{summary.get('allocation_percentage', 0)}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Room allocations
        allocations = allocation.get('allocations', [])
        if allocations:
            rooms_header = Paragraph("Room-wise Seat Allocation", self.styles['SectionHeader'])
            story.append(rooms_header)
            
            for room_alloc in allocations:
                self._add_multi_exam_room_allocation_to_story(story, room_alloc)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _add_room_allocation_to_story(self, story, room_alloc):
        """Add single room allocation details to PDF story with enhanced formatting"""
        room = room_alloc['room']
        students = room_alloc['students']
        subject_breakdown = room_alloc.get('subject_breakdown', {})
        distribution_score = room_alloc.get('distribution_score', 0)
        separation_quality = room_alloc.get('separation_quality', 0)
        
        # Room header with quality metrics
        quality_text = f" | Distribution: {distribution_score} | Separation: {separation_quality}" if distribution_score or separation_quality else ""
        room_header = Paragraph(f"Room: {room['name']} (Capacity: {room['capacity']}, Allocated: {len(students)}){quality_text}", 
                               self.styles['RoomHeader'])
        story.append(room_header)
        
        # Enhanced subject breakdown with better formatting
        if subject_breakdown:
            # Sort subjects by count for better display
            sorted_subjects = sorted(subject_breakdown.items(), key=lambda x: x[1], reverse=True)
            breakdown_text = "Subject Distribution: " + " | ".join([f"<b>{subject}</b>: {count}" for subject, count in sorted_subjects])
            breakdown_para = Paragraph(breakdown_text, self.styles['Normal'])
            story.append(breakdown_para)
            story.append(Spacer(1, 8))
        
        # Enhanced student table with better subject formatting
        if students:
            student_data = [['Seat', 'Student Name', 'Roll Number', 'Year', 'Primary Subject', 'All Subjects']]
            
            for student_alloc in sorted(students, key=lambda x: x['seat_number']):
                student = student_alloc['student']
                # Handle both single and multi-subject students
                student_subjects = student.get('subjects', [])
                if not student_subjects and student.get('subject'):
                    student_subjects = [student['subject']]
                
                # Primary subject (first one or single subject)
                primary_subject = student_subjects[0] if student_subjects else 'N/A'
                
                # Format all subjects with compact formatting for tables
                if len(student_subjects) > 1:
                    all_subjects = self._format_subjects_for_pdf(student_subjects)
                else:
                    all_subjects = primary_subject
                
                # Truncate long text to fit in columns
                primary_truncated = primary_subject[:12] + ('...' if len(primary_subject) > 12 else '')
                all_subjects_truncated = all_subjects[:20] + ('...' if len(all_subjects) > 20 else '')
                
                student_data.append([
                    str(student_alloc['seat_number']),
                    self._format_name_for_pdf(student['name']),
                    student['roll_number'],
                    str(student['year']),
                    primary_truncated,
                    all_subjects_truncated
                ])
            
            # Adjusted column widths to fit better within page margins
            student_table = Table(student_data, colWidths=[0.5*inch, 1.3*inch, 0.9*inch, 0.4*inch, 1.1*inch, 1.8*inch])
            student_table.setStyle(TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                
                # Data styling
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Seat numbers centered
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Names left-aligned
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Roll numbers centered
                ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Year centered
                ('ALIGN', (4, 1), (4, -1), 'LEFT'),    # Primary subject left-aligned
                ('ALIGN', (5, 1), (5, -1), 'LEFT'),    # All subjects left-aligned
                
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),  # Smaller font for better fit
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                
                # Alternating row colors for better readability
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgreen, colors.white]),
                
                # Grid and padding - reduced for better fit
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TOPPADDING', (0, 1), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                ('LEFTPADDING', (0, 1), (-1, -1), 3),
                ('RIGHTPADDING', (0, 1), (-1, -1), 3),
                
                # Subject column specific formatting
                ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                ('WORDWRAP', (1, 1), (-1, -1), True),
            ]))
            
            story.append(student_table)
        
        story.append(Spacer(1, 16))
    
    def _add_multi_exam_room_allocation_to_story(self, story, room_alloc):
        """Add multi-exam room allocation details to PDF story"""
        room = room_alloc['room']
        students = room_alloc['students']
        exam_breakdown = room_alloc.get('exam_breakdown', {})
        subject_breakdown = room_alloc.get('subject_breakdown', {})
        
        # Room header
        room_header = Paragraph(f"Room: {room['name']} (Capacity: {room['capacity']}, Allocated: {len(students)})", 
                               self.styles['RoomHeader'])
        story.append(room_header)
        
        # Exam and subject breakdown
        if exam_breakdown:
            exam_text = "Exam Distribution: " + ", ".join([f"{exam}: {count}" for exam, count in exam_breakdown.items()])
            exam_para = Paragraph(exam_text, self.styles['Normal'])
            story.append(exam_para)
        
        if subject_breakdown:
            subject_text = "Subject Distribution: " + ", ".join([f"{subject}: {count}" for subject, count in subject_breakdown.items()])
            subject_para = Paragraph(subject_text, self.styles['Normal'])
            story.append(subject_para)
        
        story.append(Spacer(1, 8))
        
        # Student table
        if students:
            student_data = [['Seat', 'Name', 'Roll Number', 'Year', 'Exam', 'Subject']]
            
            for student_alloc in sorted(students, key=lambda x: x['seat_number']):
                student = student_alloc['student']
                
                student_data.append([
                    str(student_alloc['seat_number']),
                    student['name'],
                    student['roll_number'],
                    str(student['year']),
                    student.get('exam_name', 'N/A'),
                    student.get('exam_subject', 'N/A')
                ])
            
            student_table = Table(student_data, colWidths=[0.6*inch, 1.4*inch, 1*inch, 0.6*inch, 1.4*inch, 1*inch])
            student_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(student_table)
        
        story.append(Spacer(1, 16))
    
    def _format_subjects_for_pdf(self, subjects):
        """Format subject list for better PDF display"""
        if not subjects:
            return 'N/A'
        
        # For table cells, use compact comma-separated format instead of line breaks
        if len(subjects) <= 2:
            return ', '.join(subjects)
        elif len(subjects) <= 4:
            return ', '.join(subjects[:3]) + f' (+{len(subjects)-3})' if len(subjects) > 3 else ', '.join(subjects)
        else:
            # For many subjects, show first 2 and count
            return f"{subjects[0]}, {subjects[1]} (+{len(subjects)-2})"
    
    def _format_name_for_pdf(self, name):
        """Format student name for better PDF display"""
        if not name:
            return 'N/A'
        
        # Truncate very long names to fit in column
        if len(name) > 20:
            return name[:17] + '...'
        return name
    
    def generate_class_specific_report(self, allocation, class_year):
        """Generate PDF report for a specific class/year showing all students from that class"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Build the document
        story = []
        
        # Title
        title = Paragraph(f"Class {class_year} Seat Allocation Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Report info
        info_data = [
            ['Generated On:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Class/Year:', f"{class_year}{'st' if class_year == '1' else 'nd' if class_year == '2' else 'rd' if class_year == '3' else 'th'} Year"],
            ['Strategy:', allocation.get('strategy', 'N/A').title()],
            ['Subject Filter:', allocation.get('subject_filter', 'All Subjects') or 'All Subjects']
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Filter students by class year and collect statistics
        class_students = []
        total_class_students = 0
        allocated_class_students = 0
        rooms_with_class_students = set()
        subject_distribution = {}
        
        allocations = allocation.get('allocations', [])
        
        for room_alloc in allocations:
            room = room_alloc['room']
            students = room_alloc['students']
            room_class_students = []
            
            for student_alloc in students:
                student = student_alloc['student']
                if str(student.get('year', '')) == str(class_year):
                    room_class_students.append(student_alloc)
                    allocated_class_students += 1
                    rooms_with_class_students.add(room['name'])
                    
                    # Track subject distribution
                    student_subjects = student.get('subjects', [])
                    if not student_subjects and student.get('subject'):
                        student_subjects = [student['subject']]
                    
                    for subject in student_subjects:
                        subject_distribution[subject] = subject_distribution.get(subject, 0) + 1
            
            if room_class_students:
                class_students.append({
                    'room': room,
                    'students': room_class_students,
                    'total_in_room': len(students),
                    'class_students_count': len(room_class_students)
                })
        
        # Calculate total class students (this would ideally come from database query)
        # For now, we'll use allocated count as minimum
        total_class_students = allocated_class_students
        
        # Class-specific summary
        summary_header = Paragraph(f"Class {class_year} Summary", self.styles['SectionHeader'])
        story.append(summary_header)
        
        summary_data = [
            ['Total Class Students:', str(total_class_students)],
            ['Students Allocated:', str(allocated_class_students)],
            ['Students Unallocated:', str(total_class_students - allocated_class_students)],
            ['Rooms with Class Students:', str(len(rooms_with_class_students))],
            ['Allocation Rate:', f"{(allocated_class_students/total_class_students*100):.1f}%" if total_class_students > 0 else "0%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Subject distribution for the class
        if subject_distribution:
            subject_header = Paragraph(f"Subject Distribution - Class {class_year}", self.styles['SectionHeader'])
            story.append(subject_header)
            
            # Sort subjects by count
            sorted_subjects = sorted(subject_distribution.items(), key=lambda x: x[1], reverse=True)
            subject_data = [['Subject', 'Number of Students', 'Percentage']]
            
            for subject, count in sorted_subjects:
                percentage = (count / allocated_class_students * 100) if allocated_class_students > 0 else 0
                subject_data.append([subject, str(count), f"{percentage:.1f}%"])
            
            # Add total row
            subject_data.append(['Total', str(allocated_class_students), '100.0%'])
            
            subject_table = Table(subject_data, colWidths=[2*inch, 1.5*inch, 1*inch])
            subject_table.setStyle(TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Data styling
                ('ALIGN', (0, 1), (0, -2), 'LEFT'),    # Subject names left-aligned
                ('ALIGN', (1, 1), (-1, -2), 'CENTER'), # Numbers centered
                ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -2), 9),
                ('BACKGROUND', (0, 1), (-1, -2), colors.lightgreen),
                
                # Total row styling
                ('BACKGROUND', (0, -1), (-1, -1), colors.darkgreen),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(subject_table)
            story.append(Spacer(1, 20))
        
        # Room-wise allocation details for class students
        if class_students:
            rooms_header = Paragraph(f"Room-wise Allocation - Class {class_year} Students", self.styles['SectionHeader'])
            story.append(rooms_header)
            
            # Sort rooms by name for consistent ordering
            class_students.sort(key=lambda x: x['room']['name'])
            
            for room_data in class_students:
                self._add_class_room_allocation_to_story(story, room_data, class_year)
        else:
            no_students_para = Paragraph(f"No students from Class {class_year} were allocated in this allocation.", 
                                       self.styles['Normal'])
            story.append(no_students_para)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _add_class_room_allocation_to_story(self, story, room_data, class_year):
        """Add class-specific room allocation details to PDF story"""
        room = room_data['room']
        students = room_data['students']
        total_in_room = room_data['total_in_room']
        class_students_count = room_data['class_students_count']
        
        # Room header with class-specific info
        room_header = Paragraph(
            f"<b>Room:</b> {room['name']} | <b>Class {class_year} Students:</b> {class_students_count}/{total_in_room} | <b>Room Capacity:</b> {room['capacity']}", 
            self.styles['RoomHeader']
        )
        story.append(room_header)
        
        # Subject breakdown for class students in this room
        subject_breakdown = {}
        for student_alloc in students:
            student = student_alloc['student']
            student_subjects = student.get('subjects', [])
            if not student_subjects and student.get('subject'):
                student_subjects = [student['subject']]
            
            for subject in student_subjects:
                subject_breakdown[subject] = subject_breakdown.get(subject, 0) + 1
        
        if subject_breakdown:
            sorted_subjects = sorted(subject_breakdown.items(), key=lambda x: x[1], reverse=True)
            breakdown_text = "<b>Subject Distribution:</b> " + " | ".join([f"{subject}: {count}" for subject, count in sorted_subjects])
            breakdown_para = Paragraph(breakdown_text, self.styles['Normal'])
            story.append(breakdown_para)
            story.append(Spacer(1, 8))
        
        # Student table with proper formatting and fixed column widths
        if students:
            student_data = [['Seat', 'Student Name', 'Roll Number', 'Primary Subject', 'All Subjects']]
            
            for student_alloc in sorted(students, key=lambda x: x['seat_number']):
                student = student_alloc['student']
                student_subjects = student.get('subjects', [])
                if not student_subjects and student.get('subject'):
                    student_subjects = [student['subject']]
                
                # Primary subject (first one or single subject)
                primary_subject = student_subjects[0] if student_subjects else 'N/A'
                
                # Format all subjects with better line breaks and truncation
                if len(student_subjects) > 1:
                    # Limit to 3 subjects max and format compactly
                    display_subjects = student_subjects[:3]
                    if len(student_subjects) > 3:
                        all_subjects_text = ', '.join(display_subjects) + f' (+{len(student_subjects)-3})'
                    else:
                        all_subjects_text = ', '.join(display_subjects)
                else:
                    all_subjects_text = primary_subject
                
                # Ensure text fits in columns by truncating if necessary
                if len(all_subjects_text) > 25:
                    all_subjects_text = all_subjects_text[:22] + '...'
                
                student_data.append([
                    str(student_alloc['seat_number']),
                    self._format_name_for_pdf(student['name']),
                    student['roll_number'],
                    primary_subject[:15] + ('...' if len(primary_subject) > 15 else ''),  # Truncate long subjects
                    all_subjects_text
                ])
            
            # Adjusted column widths to fit within page margins better
            student_table = Table(student_data, colWidths=[0.6*inch, 1.4*inch, 1.0*inch, 1.3*inch, 1.7*inch])
            student_table.setStyle(TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                
                # Data styling
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Seat numbers centered
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Names left-aligned
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Roll numbers centered
                ('ALIGN', (3, 1), (3, -1), 'LEFT'),    # Primary subject left-aligned
                ('ALIGN', (4, 1), (4, -1), 'LEFT'),    # All subjects left-aligned
                
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),  # Smaller font for data
                
                # Alternating row colors for better readability
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightblue, colors.white]),
                
                # Grid and padding - reduced padding for better fit
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TOPPADDING', (0, 1), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                ('LEFTPADDING', (0, 1), (-1, -1), 3),
                ('RIGHTPADDING', (0, 1), (-1, -1), 3),
                ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                
                # Word wrap for text cells
                ('WORDWRAP', (1, 1), (-1, -1), True),
            ]))
            
            story.append(student_table)
        
        story.append(Spacer(1, 16))