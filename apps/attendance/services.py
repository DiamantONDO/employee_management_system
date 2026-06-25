from django.core.exceptions import ValidationError
from apps.attendance.repositories import AttendanceRepository
from apps.employees.repositories import EmployeeRepository


class AttendanceService:

    def __init__(self):
        self.repo = AttendanceRepository()
        self.employee_repo = EmployeeRepository()

    def get_all_attendance(self, filters=None):
        if filters is None:
            filters = {}
        return self.repo.get_all(**filters)

    def get_attendance_by_id(self, attendance_id):
        attendance = self.repo.get_by_id(attendance_id)
        if not attendance:
            raise ValidationError({"detail": "Attendance record not found."})
        return attendance

    def create_attendance(self, data):
        employee_id = data.get('employee_id') or (data.get('employee').id if data.get('employee') else None)

        # Check employee exists
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise ValidationError({"employee": "Employee not found."})

        # Check no duplicate attendance for same day
        existing = self.repo.get_by_employee_and_date(
            employee_id=employee_id,
            date=data.get('attendance_date')
        )
        if existing:
            raise ValidationError({"detail": "Attendance record already exists for this employee on this date."})

        return self.repo.create(**data)

    def update_attendance(self, attendance_id, data):
        attendance = self.get_attendance_by_id(attendance_id)
        return self.repo.update(attendance, **data)

    def delete_attendance(self, attendance_id):
        attendance = self.get_attendance_by_id(attendance_id)
        self.repo.soft_delete(attendance)
        return True

    def get_employee_attendance(self, employee_id):
        return self.repo.filter_by_employee(employee_id)

    def get_attendance_by_date_range(self, start_date, end_date):
        return self.repo.filter_by_date_range(start_date, end_date)