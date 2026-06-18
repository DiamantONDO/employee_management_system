from django.core.exceptions import ValidationError
from apps.employees.repositories import EmployeeRepository

class EmployeeService:

    def __init__(self):
        self.repo = EmployeeRepository()

    def get_all_employees(self, filters=None):
        if filters is None:
            filters = {}
        return self.repo.get_all(**filters)

    def get_employee_by_id(self, employee_id):
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise ValidationError({"detail": 'Employee not found'})
        return employee

    def create_employee(self, data):
        if self.repo.get_by_email(data.get('email')):
            raise ValidationError('Employee with this email already exists')

        if self.repo.get_by_code(data.get('employee_code')):
            raise ValidationError({"detail": 'Employee with this code already exists'})

        return self.repo.create(**data)

    def update_employee(self, employee_id, data):
        employee = self.get_employee_by_id(employee_id)

        # Check email uniqueness if email is being changed
        if 'email' in data and data['email'] != employee.email:
            if self.repo.get_by_email(data['email']):
                raise ValidationError({"email": "An employee with this email already exists."})

        return self.repo.update(employee, **data)

    def delete_employee(self, employee_id):
        employee = self.get_employee_by_id(employee_id)
        self.repo.soft_delete(employee)
        return True

    def search_employees(self, name):
        return self.repo.search_by_name(name)

    def filter_employees(self, department=None, is_active=None):
        if department:
            return self.repo.filter_by_department(department)
        if is_active is not None:
            return self.repo.filter_by_active(is_active)
        return self.repo.get_all()