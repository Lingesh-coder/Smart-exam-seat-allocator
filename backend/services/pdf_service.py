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
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)

        story = []

        title = Paragraph("Exam Seat Allocation Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))

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

        allocations = allocation.get('allocations', [])
        if allocations:
            rooms_header = Paragraph("Room-wise Seat Allocation", self.styles['SectionHeader'])
            story.append(rooms_header)

            for room_alloc in allocations:
                self._add_room_allocation_to_story(story, room_alloc)

        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_multi_exam_report(self, allocation):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)

        story = []

        title = Paragraph("Multi-Exam Seat Allocation Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))

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

        allocations = allocation.get('allocations', [])
        if allocations:
            rooms_header = Paragraph("Room-wise Seat Allocation", self.styles['SectionHeader'])
            story.append(rooms_header)

            for room_alloc in allocations:
                self._add_multi_exam_room_allocation_to_story(story, room_alloc)

        doc.build(story)
        buffer.seek(0)
        return buffer

    def _add_room_allocation_to_story(self, story, room_alloc):
        room = room_alloc['room']
        students = room_alloc['students']
        subject_breakdown = room_alloc.get('subject_breakdown', {})
        distribution_score = room_alloc.get('distribution_score', 0)
        separation_quality = room_alloc.get('separation_quality', 0)

        quality_text = f" | Distribution: {distribution_score} | Separation: {separation_quality}" if distribution_score or separation_quality else ""
        room_header = Paragraph(f"Room: {room['name']} (Capacity: {room['capacity']}, Allocated: {len(students)}){quality_text}",
                               self.styles['RoomHeader'])
        story.append(room_header)

        if subject_breakdown:
            sorted_subjects = sorted(subject_breakdown.items(), key=lambda x: x[1], reverse=True)
            breakdown_text = "Subject Distribution: " + " | ".join([f"<b>{subject}</b>: {count}" for subject, count in sorted_subjects])
            breakdown_para = Paragraph(breakdown_text, self.styles['Normal'])
            story.append(breakdown_para)
            story.append(Spacer(1, 8))

        if students:
            student_data = [['Seat', 'Roll Number', 'Year', 'Primary Subject', 'All Subjects']]

            for student_alloc in sorted(students, key=lambda x: x['seat_number']):
                student = student_alloc['student']
                student_subjects = student.get('subjects', [])
                if not student_subjects and student.get('subject'):
                    student_subjects = [student['subject']]

                primary_subject = student_subjects[0] if student_subjects else 'N/A'

                if len(student_subjects) > 1:
                    all_subjects = self._format_subjects_for_pdf(student_subjects)
                else:
                    all_subjects = primary_subject

                primary_truncated = primary_subject[:12] + ('...' if len(primary_subject) > 12 else '')
                all_subjects_truncated = all_subjects[:20] + ('...' if len(all_subjects) > 20 else '')

                student_data.append([
                    str(student_alloc['seat_number']),
                    student['roll_number'],
                    str(student['year']),
                    primary_truncated,
                    all_subjects_truncated
                ])

            student_table = Table(student_data, colWidths=[0.5*inch, 1.2*inch, 0.4*inch, 1.3*inch, 2.6*inch])
            student_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('ALIGN', (3, 1), (3, -1), 'LEFT'),
                ('ALIGN', (4, 1), (4, -1), 'LEFT'),

                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),

                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgreen, colors.white]),

                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TOPPADDING', (0, 1), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                ('LEFTPADDING', (0, 1), (-1, -1), 3),
                ('RIGHTPADDING', (0, 1), (-1, -1), 3),

                ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                ('WORDWRAP', (1, 1), (-1, -1), True),
            ]))

            story.append(student_table)

        story.append(Spacer(1, 16))

    def _add_multi_exam_room_allocation_to_story(self, story, room_alloc):
        room = room_alloc['room']
        students = room_alloc['students']
        exam_breakdown = room_alloc.get('exam_breakdown', {})
        subject_breakdown = room_alloc.get('subject_breakdown', {})

        room_header = Paragraph(f"Room: {room['name']} (Capacity: {room['capacity']}, Allocated: {len(students)})",
                               self.styles['RoomHeader'])
        story.append(room_header)

        if exam_breakdown:
            exam_text = "Exam Distribution: " + ", ".join([f"{exam}: {count}" for exam, count in exam_breakdown.items()])
            exam_para = Paragraph(exam_text, self.styles['Normal'])
            story.append(exam_para)

        if subject_breakdown:
            subject_text = "Subject Distribution: " + ", ".join([f"{subject}: {count}" for subject, count in subject_breakdown.items()])
            subject_para = Paragraph(subject_text, self.styles['Normal'])
            story.append(subject_para)

        story.append(Spacer(1, 8))

        if students:
            student_data = [['Seat', 'Roll Number', 'Year', 'Exam', 'Subject']]

            for student_alloc in sorted(students, key=lambda x: x['seat_number']):
                student = student_alloc['student']

                student_data.append([
                    str(student_alloc['seat_number']),
                    student['roll_number'],
                    str(student['year']),
                    student.get('exam_name', 'N/A'),
                    student.get('exam_subject', 'N/A')
                ])

            student_table = Table(student_data, colWidths=[0.6*inch, 1.2*inch, 0.6*inch, 1.8*inch, 1.8*inch])
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
                if not subjects:
            return 'N/A'

        if len(subjects) <= 2:
            return ', '.join(subjects)
        elif len(subjects) <= 4:
            return ', '.join(subjects[:3]) + f' (+{len(subjects)-3})' if len(subjects) > 3 else ', '.join(subjects)
        else:
            return f"{subjects[0]}, {subjects[1]} (+{len(subjects)-2})"

    def generate_class_specific_report(self, allocation, class_year):
                buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)

        story = []

        title = Paragraph(f"Class {class_year} Seat Allocation Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))

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

        total_class_students = allocated_class_students

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

        if subject_distribution:
            subject_header = Paragraph(f"Subject Distribution - Class {class_year}", self.styles['SectionHeader'])
            story.append(subject_header)

            sorted_subjects = sorted(subject_distribution.items(), key=lambda x: x[1], reverse=True)
            subject_data = [['Subject', 'Number of Students', 'Percentage']]

            for subject, count in sorted_subjects:
                percentage = (count / allocated_class_students * 100) if allocated_class_students > 0 else 0
                subject_data.append([subject, str(count), f"{percentage:.1f}%"])

            subject_data.append(['Total', str(allocated_class_students), '100.0%'])

            subject_table = Table(subject_data, colWidths=[2*inch, 1.5*inch, 1*inch])
            subject_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

                ('ALIGN', (0, 1), (0, -2), 'LEFT'),
                ('ALIGN', (1, 1), (-1, -2), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -2), 9),
                ('BACKGROUND', (0, 1), (-1, -2), colors.lightgreen),

                ('BACKGROUND', (0, -1), (-1, -1), colors.darkgreen),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),

                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(subject_table)
            story.append(Spacer(1, 20))

        if class_students:
            rooms_header = Paragraph(f"Room-wise Allocation - Class {class_year} Students", self.styles['SectionHeader'])
            story.append(rooms_header)

            class_students.sort(key=lambda x: x['room']['name'])

            for room_data in class_students:
                self._add_class_room_allocation_to_story(story, room_data, class_year)
        else:
            no_students_para = Paragraph(f"No students from Class {class_year} were allocated in this allocation.",
                                       self.styles['Normal'])
            story.append(no_students_para)

        doc.build(story)
        buffer.seek(0)
        return buffer

    def _add_class_room_allocation_to_story(self, story, room_data, class_year):
                room = room_data['room']
        students = room_data['students']
        total_in_room = room_data['total_in_room']
        class_students_count = room_data['class_students_count']

        room_header = Paragraph(
            f"<b>Room:</b> {room['name']} | <b>Class {class_year} Students:</b> {class_students_count}/{total_in_room} | <b>Room Capacity:</b> {room['capacity']}",
            self.styles['RoomHeader']
        )
        story.append(room_header)

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

        if students:
            student_data = [['Seat', 'Roll Number', 'Primary Subject', 'All Subjects']]

            for student_alloc in sorted(students, key=lambda x: x['seat_number']):
                student = student_alloc['student']
                student_subjects = student.get('subjects', [])
                if not student_subjects and student.get('subject'):
                    student_subjects = [student['subject']]

                primary_subject = student_subjects[0] if student_subjects else 'N/A'

                if len(student_subjects) > 1:
                    display_subjects = student_subjects[:3]
                    if len(student_subjects) > 3:
                        all_subjects_text = ', '.join(display_subjects) + f' (+{len(student_subjects)-3})'
                    else:
                        all_subjects_text = ', '.join(display_subjects)
                else:
                    all_subjects_text = primary_subject

                if len(all_subjects_text) > 25:
                    all_subjects_text = all_subjects_text[:22] + '...'

                student_data.append([
                    str(student_alloc['seat_number']),
                    student['roll_number'],
                    primary_subject[:15] + ('...' if len(primary_subject) > 15 else ''),
                    all_subjects_text
                ])

            student_table = Table(student_data, colWidths=[0.6*inch, 1.2*inch, 1.8*inch, 2.4*inch])
            student_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                ('ALIGN', (3, 1), (3, -1), 'LEFT'),

                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),

                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightblue, colors.white]),

                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TOPPADDING', (0, 1), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                ('LEFTPADDING', (0, 1), (-1, -1), 3),
                ('RIGHTPADDING', (0, 1), (-1, -1), 3),
                ('VALIGN', (0, 1), (-1, -1), 'TOP'),

                ('WORDWRAP', (1, 1), (-1, -1), True),
            ]))

            story.append(student_table)

        story.append(Spacer(1, 16))
