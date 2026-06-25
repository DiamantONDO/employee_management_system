from django.db import models
import uuid
from django.db import models
from apps.employees.models import Employee

# Create your models here.
class Attendance(models.Model):
    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("LATE", "Late"),
        ("HALF DAY", "Half Day"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    status = models.CharField(choices=STATUS_CHOICES, default="PRESENT", max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-attendance_date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        unique_together = ['employee', 'attendance_date']

    def __str__(self):
        return f"{self.employee.first_name} - {self.attendance_date} - {self.status}"