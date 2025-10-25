from flask import Blueprint, request, jsonify, send_file
from models.database import Allocation, Student, Room
from services.allocation_service import AllocationService
from services.excel_service import ExcelService
from utils.json_utils import serialize_document
import tempfile
import os

allocations_bp = Blueprint('allocations', __name__)

@allocations_bp.route('/allocations', methods=['GET'])
def get_allocations():
    try:
        allocations = Allocation.get_all()
        return jsonify([serialize_document(allocation) for allocation in allocations])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@allocations_bp.route('/allocations', methods=['POST'])
def create_allocation():
    try:
        data = request.get_json()
        strategy = data.get('strategy', 'mixed')
        subject_filter = data.get('subject_filter', '')

        students_raw = Student.get_all()
        rooms_raw = Room.get_all()

        if not students_raw:
            return jsonify({'error': 'No students found'}), 400
        if not rooms_raw:
            return jsonify({'error': 'No rooms found'}), 400

        students = [serialize_document(s) for s in students_raw]
        rooms = [serialize_document(r) for r in rooms_raw]

        if subject_filter:
            students = [s for s in students if subject_filter in (s.get('subjects', []) or [s.get('subject', '')])]
            if not students:
                return jsonify({'error': f'No students found for subject: {subject_filter}'}), 400

        allocation_service = AllocationService()
        result = allocation_service.allocate_seats(students, rooms, strategy)

        allocation_id = Allocation.create(
            strategy=strategy,
            subject_filter=subject_filter,
            allocations=result['allocations'],
            allocation_summary=result['summary']
        )

        return jsonify({
            'message': 'Allocation created successfully',
            'allocation_id': str(allocation_id),
            'allocation': serialize_document(result)
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@allocations_bp.route('/allocations/<allocation_id>', methods=['GET'])
def get_allocation(allocation_id):
    try:
        allocation = Allocation.get_by_id(allocation_id)
        if allocation:
            return jsonify(serialize_document(allocation))
        return jsonify({'error': 'Allocation not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@allocations_bp.route('/allocations/latest', methods=['GET'])
def get_latest_allocation():
    try:
        allocation = Allocation.get_latest()
        if allocation:
            return jsonify(serialize_document(allocation))
        return jsonify({'error': 'No allocations found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@allocations_bp.route('/allocations/<allocation_id>/report', methods=['GET'])
def generate_allocation_report(allocation_id):
    try:
        allocation_raw = Allocation.get_by_id(allocation_id)
        if not allocation_raw:
            return jsonify({'error': 'Allocation not found'}), 404

        allocation = serialize_document(allocation_raw)

        excel_service = ExcelService()

        if allocation.get('type') == 'multi_exam':
            excel_buffer = excel_service.generate_multi_exam_report(allocation)
            filename = f"multi_exam_allocation_report_{allocation_id}.xlsx"
        else:
            excel_buffer = excel_service.generate_allocation_report(allocation)
            filename = f"allocation_report_{allocation_id}.xlsx"

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        temp_file.write(excel_buffer.getvalue())
        temp_file.close()

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            if 'temp_file' in locals():
                os.unlink(temp_file.name)
        except:
            pass

@allocations_bp.route('/allocations/<allocation_id>/class-report/<class_year>', methods=['GET'])
def generate_class_report(allocation_id, class_year):
    try:
        allocation_raw = Allocation.get_by_id(allocation_id)
        if not allocation_raw:
            return jsonify({'error': 'Allocation not found'}), 404

        if class_year not in ['1','2','3','4']:
            return jsonify({'error': 'Invalid class year. Must be 1, 2, 3, or 4'}), 400

        allocation = serialize_document(allocation_raw)

        excel_service = ExcelService()
        excel_buffer = excel_service.generate_class_specific_report(allocation, class_year)
        filename = f"class_{class_year}_allocation_report_{allocation_id}.xlsx"

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        temp_file.write(excel_buffer.getvalue())
        temp_file.close()

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            if 'temp_file' in locals():
                os.unlink(temp_file.name)
        except:
            pass

@allocations_bp.route('/allocations/<allocation_id>/classes', methods=['GET'])
def get_allocation_classes(allocation_id):
    try:
        allocation_raw = Allocation.get_by_id(allocation_id)
        if not allocation_raw:
            return jsonify({'error': 'Allocation not found'}), 404

        allocation = serialize_document(allocation_raw)

        classes = set()
        class_stats = {}

        allocations = allocation.get('allocations', [])
        for room_alloc in allocations:
            students = room_alloc['students']
            for student_alloc in students:
                student = student_alloc['student']
                year = str(student.get('year', ''))
                if year and year in ['1', '2', '3', '4']:
                    classes.add(year)
                    if year not in class_stats:
                        class_stats[year] = {'count': 0, 'rooms': set()}
                    class_stats[year]['count'] += 1
                    class_stats[year]['rooms'].add(room_alloc['room']['name'])

        for year in class_stats:
            class_stats[year]['rooms'] = list(class_stats[year]['rooms'])

        return jsonify({
            'classes': sorted(list(classes)),
            'class_statistics': class_stats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@allocations_bp.route('/allocations/<allocation_id>', methods=['DELETE'])
def delete_allocation(allocation_id):
    try:
        result = Allocation.delete(allocation_id)
        if result.deleted_count:
            return jsonify({'message': 'Allocation deleted successfully'})
        return jsonify({'error': 'Allocation not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@allocations_bp.route('/allocations/all', methods=['DELETE'])
def delete_all_allocations():
    try:
        result = Allocation.delete_all()
        return jsonify({
            'message': f'Successfully deleted {result.deleted_count} allocations',
            'deleted_count': result.deleted_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
