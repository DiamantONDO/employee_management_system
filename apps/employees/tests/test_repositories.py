from unittest import result

import pytest
from apps.employees.repositories import EmployeeRepository
from apps.employees.tests.factories import EmployeeFactory

@pytest.mark.django_db
class TestEmployeeRepository:

    def setup_method(self):
        self.repo = EmployeeRepository()

    def test_create(self):
        employee = EmployeeFactory()
        assert employee.id is not None
        assert employee.is_active is True

    def test_get_by_id(self):
        employee = EmployeeFactory()
        result = self.repo.get_by_id(employee.id)
        assert employee == result

    def get_by_id_not_found(self):
        import uuid
        result = self.repo.get_by_id(uuid.uuid4())
        assert result is None

    def test_get_by_email(self):
        employee = EmployeeFactory()
        result = self.repo.get_by_email(employee.email)
        assert employee == employee

    def test_get_by_code(self):
        employee = EmployeeFactory()
        result = self.repo.get_by_code(employee.employee_code)
        assert result == employee

    def test_get_all(self):
        EmployeeFactory.create_batch(3)
        results = self.repo.get_all()
        assert results.count() == 3

    def test_update(self):
        employee = EmployeeFactory()
        updated = self.repo.update(employee, first_name='Anthony')
        assert updated.first_name == 'Anthony'

    def test_soft_delete(self):
        employee = EmployeeFactory()
        self.repo.soft_delete(employee)
        assert employee.is_active is False

    def test_search_by_name(self):
        employee = EmployeeFactory(first_name='Anthony')
        results = self.repo.search_by_name('Anthony')
        assert employee in results

    def test_filter_by_department(self):
        EmployeeFactory(department='IT')
        EmployeeFactory(department='HR')
        results = self.repo.filter_by_department('IT')
        assert all(e.department == 'IT' for e in results)

    def test_filter_by_active(self):
        EmployeeFactory(is_active=True)
        EmployeeFactory(is_active=False)
        results = self.repo.filter_by_active(True)
        assert all(e.is_active for e in results)