import pytest
from django.core.exceptions import ValidationError
from apps.employees.services import EmployeeService
from apps.employees.tests.factories import EmployeeFactory


@pytest.mark.django_db
class TestEmployeeService:

    def setup_method(self):
        self.service = EmployeeService()

    def test_get_all_employees(self):
        EmployeeFactory.create_batch(3)
        results = self.service.get_all_employees()
        assert results.count() == 3

    def test_get_employee_by_id(self):
        employee = EmployeeFactory()
        result = self.service.get_employee_by_id(employee.id)
        assert result == employee

    def test_get_employee_by_id_not_found(self):
        import uuid
        with pytest.raises(ValidationError):
            self.service.get_employee_by_id(uuid.uuid4())

    def test_create_employee(self):
        data = {
            'employee_code': 'EMP001',
            'first_name': 'Diamant',
            'last_name': 'Anthony',
            'email': 'diamant@company.com',
            'department': 'IT',
            'position': 'Developer',
            'date_joined': '2026-01-01',
        }
        employee = self.service.create_employee(data)
        assert employee.id is not None
        assert employee.first_name == 'Diamant'

    def test_create_employee_duplicate_email(self):
        employee = EmployeeFactory()
        data = {
            'employee_code': 'EMP999',
            'first_name': 'Test',
            'last_name': 'User',
            'email': employee.email,
            'department': 'IT',
            'position': 'Developer',
            'date_joined': '2026-01-01',
        }
        with pytest.raises(ValidationError):
            self.service.create_employee(data)

    def test_update_employee(self):
        employee = EmployeeFactory()
        updated = self.service.update_employee(employee.id, {'first_name': 'Updated'})
        assert updated.first_name == 'Updated'

    def test_delete_employee_soft(self):
        employee = EmployeeFactory()
        self.service.delete_employee(employee.id)
        employee.refresh_from_db()
        assert employee.is_active is False

    def test_search_employees(self):
        EmployeeFactory(first_name='Diamant')
        results = self.service.search_employees('Diamant')
        assert results.count() >= 1

    def test_filter_by_department(self):
        EmployeeFactory(department='IT')
        EmployeeFactory(department='HR')
        results = self.service.filter_employees(department='IT')
        assert all(e.department == 'IT' for e in results)