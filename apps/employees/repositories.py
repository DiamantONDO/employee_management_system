from apps.employees.models import Employee


class EmployeeRepository:

    def get_all(self, **filters):
        return Employee.objects.filter(**filters)

    def get_by_id(self, employee_id):
        return Employee.objects.filter(id=employee_id).first()

    def get_by_name(self, employee_name):
        return Employee.objects.filter(employee_name=employee_name).first()

    def get_by_email(self, email):
        return Employee.objects.filter(email=email).first()

    def get_by_code(self, employee_code):
        return Employee.objects.filter(employee_code=employee_code).first()

    def create(self, **kwargs):
        return Employee.objects.create(**kwargs)

    def update(self, employee, **kwargs):
        for key, value in kwargs.items():
            setattr(employee, key, value)
        employee.save()
        return employee

    #Soft delete: instead of removing the record from the database,
    # it just sets is_active = False
    def soft_delete(self, employee):
        employee.is_active = False
        employee.save()
        return employee

    def delete(self, employee):
        employee.delete()

    def search_by_name(self, name):
        return Employee.objects.filter(
            first_name__icontains=name
        ) | Employee.objects.filter(
            last_name__icontains=name
        )

    def filter_by_department(self, department):
        return Employee.objects.filter(
            department=department
        )

    def filter_by_active(self, is_active):
        return Employee.objects.filter(is_active=is_active)