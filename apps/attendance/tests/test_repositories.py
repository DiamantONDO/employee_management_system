import pytest
from apps.attendance.repositories import AttendanceRepository
from apps.attendance.tests.factories import AttendanceFactory
from apps.employees.tests.factories import EmployeeFactory
from datetime import date, timedelta


@pytest.mark.django_db
class TestAttendanceRepository:

    def setup_method(self):
        self.repo = AttendanceRepository()

    def test_create(self):
        attendance = AttendanceFactory()
        assert attendance.id is not None

    def test_get_by_id(self):
        attendance = AttendanceFactory()
        result = self.repo.get_by_id(attendance.id)
        assert result == attendance

    def test_get_by_id_not_found(self):
        import uuid
        result = self.repo.get_by_id(uuid.uuid4())
        assert result is None

    def test_get_all(self):
        AttendanceFactory.create_batch(3)
        results = self.repo.get_all()
        assert results.count() == 3

    def test_filter_by_employee(self):
        employee = EmployeeFactory()
        AttendanceFactory(employee=employee)
        AttendanceFactory()
        results = self.repo.filter_by_employee(employee.id)
        assert all(a.employee == employee for a in results)

    def test_filter_by_status(self):
        AttendanceFactory(status='PRESENT')
        AttendanceFactory(status='ABSENT')
        results = self.repo.filter_by_status('PRESENT')
        assert all(a.status == 'PRESENT' for a in results)

    def test_filter_by_date(self):
        today = date.today()
        AttendanceFactory(attendance_date=today)
        results = self.repo.filter_by_date(today)
        assert results.count() >= 1

    def test_filter_by_date_range(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        AttendanceFactory(attendance_date=today)
        AttendanceFactory(attendance_date=yesterday)
        results = self.repo.filter_by_date_range(yesterday, today)
        assert results.count() == 2

    def test_soft_delete_not_applicable(self):
        attendance = AttendanceFactory()
        self.repo.soft_delete(attendance)
        result = self.repo.get_by_id(attendance.id)
        assert result is None