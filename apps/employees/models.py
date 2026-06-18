from django.db import models
import uuid
from django.db import models
from django.db.models.fields import DateField


# Create your models here.
class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ("IT", "Information Technology"),
        ("HR", "Human Resources & Human"),
        ("FINANCE", "Finance"),
        ("MARKETING", "Marketing"),
        ("SALES", "Sales"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_code = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    position = models.CharField(max_length=100)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_code})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
