"""
PDF report generation service
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
        
        # Summary
        summary = allocation.get('allocation_summary', {})
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
        """Add single room allocation details to PDF story"""
        room = room_alloc['room']
        students = room_alloc['students']
        subject_breakdown = room_alloc.get('subject_breakdown', {})
        
        # Room header
        room_header = Paragraph(f"Room: {room['name']} (Capacity: {room['capacity']}, Allocated: {len(students)})", 
                               self.styles['RoomHeader'])
        story.append(room_header)
        
        # Subject breakdown
        if subject_breakdown:
            breakdown_text = "Subject Distribution: " + ", ".join([f"{subject}: {count}" for subject, count in subject_breakdown.items()])
            breakdown_para = Paragraph(breakdown_text, self.styles['Normal'])
            story.append(breakdown_para)
            story.append(Spacer(1, 8))
        
        # Student table
        if students:
            student_data = [['Seat', 'Name', 'Roll Number', 'Year', 'Subject']]
            
            for student_alloc in sorted(students, key=lambda x: x['seat_number']):
                student = student_alloc['student']
                # Handle both single and multi-subject students
                student_subjects = student.get('subjects', [])
                if not student_subjects and student.get('subject'):
                    student_subjects = [student['subject']]
                subject_display = ', '.join(student_subjects) if student_subjects else 'N/A'
                
                student_data.append([
                    str(student_alloc['seat_number']),
                    student['name'],
                    student['roll_number'],
                    str(student['year']),
                    subject_display
                ])
            
            student_table = Table(student_data, colWidths=[0.8*inch, 1.8*inch, 1.2*inch, 0.8*inch, 1.4*inch])
            student_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
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
