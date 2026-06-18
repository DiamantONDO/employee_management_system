import pytest
from django.core.exceptions import ValidationError
from apps.attendance.services import AttendanceService
from apps.attendance.tests.factories import AttendanceFactory
from apps.employees.tests.factories import EmployeeFactory
from datetime import date


@pytest.mark.django_db
class TestAttendanceService:

    def setup_method(self):
        self.service = AttendanceService()

    def test_get_all_attendance(self):
        AttendanceFactory.create_batch(3)
        results = self.service.get_all_attendance()
        assert results.count() == 3

    def test_get_attendance_by_id(self):
        attendance = AttendanceFactory()
        result = self.service.get_attendance_by_id(attendance.id)
        assert result == attendance

    def test_get_attendance_by_id_not_found(self):
        import uuid
        with pytest.raises(ValidationError):
            self.service.get_attendance_by_id(uuid.uuid4())

    def test_create_attendance(self):
        employee = EmployeeFactory()
        data = {
            'employee': employee,
            'attendance_date': date.today(),
            'status': 'PRESENT',
            'check_in_time': '09:00:00',
            'check_out_time': '17:00:00',
        }
        attendance = self.service.create_attendance(data)
        assert attendance.id is not None

    def test_create_attendance_duplicate(self):
        attendance = AttendanceFactory()
        data = {
            'employee': attendance.employee,
            'attendance_date': attendance.attendance_date,
            'status': 'PRESENT',
        }
        with pytest.raises(ValidationError):
            self.service.create_attendance(data)

    def test_update_attendance(self):
        attendance = AttendanceFactory()
        updated = self.service.update_attendance(attendance.id, {'status': 'LATE'})
        assert updated.status == 'LATE'

    def test_delete_attendance(self):
        attendance = AttendanceFactory()
        self.service.delete_attendance(attendance.id)
        with pytest.raises(ValidationError):
            self.service.get_attendance_by_id(attendance.id)

    def test_get_employee_attendance(self):
        employee = EmployeeFactory()
        AttendanceFactory(employee=employee)
        results = self.service.get_employee_attendance(employee.id)
        assert results.count() == 1