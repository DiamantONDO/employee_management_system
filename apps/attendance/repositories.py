from apps.attendance.models import Attendance


class AttendanceRepository:

    def get_all(self, **filters):
        return Attendance.objects.select_related('employee').filter(**filters)

    def get_by_id(self, attendance_id):
        return Attendance.objects.select_related('employee').filter(id=attendance_id).first()

    def create(self, **kwargs):
        return Attendance.objects.create(**kwargs)

    def update(self, attendance, **kwargs):
        for key, value in kwargs.items():
            setattr(attendance, key, value)
        attendance.save()
        return attendance

    def delete(self, attendance):
        attendance.delete()

    def filter_by_employee(self, employee_id):
        return Attendance.objects.select_related('employee').filter(employee_id=employee_id)

    def filter_by_status(self, status):
        return Attendance.objects.select_related('employee').filter(status=status)

    def filter_by_date(self, date):
        return Attendance.objects.select_related('employee').filter(attendance_date=date)

    def filter_by_date_range(self, start_date, end_date):
        return Attendance.objects.select_related('employee').filter(
            attendance_date__gte=start_date,
            attendance_date__lte=end_date
        )

    def get_by_employee_and_date(self, employee_id, date):
        return Attendance.objects.filter(
            employee_id=employee_id,
            attendance_date=date
        ).first()