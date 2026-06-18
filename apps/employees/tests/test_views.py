import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.employees.tests.factories import EmployeeFactory
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client():
    client = APIClient()
    user = User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='Test1234!'
    )
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.mark.django_db
class TestEmployeeViews:

    def test_list_employees_unauthenticated(self, api_client):
        response = api_client.get('/api/v1/employees/')
        assert response.status_code == 401

    def test_list_employees_authenticated(self, auth_client):
        EmployeeFactory.create_batch(3)
        response = auth_client.get('/api/v1/employees/')
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_employee(self, auth_client):
        data = {
            'employee_code': 'EMP001',
            'first_name': 'Diamant',
            'last_name': 'Anthony',
            'email': 'diamant@company.com',
            'department': 'IT',
            'position': 'Developer',
            'date_joined': '2026-01-01',
        }
        response = auth_client.post('/api/v1/employees/', data, format='json')
        print(response.data)
        assert response.status_code == 201
        assert response.data['first_name'] == 'Diamant'

    def test_create_employee_duplicate_email(self, auth_client):
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
        response = auth_client.post('/api/v1/employees/', data, format='json')
        assert response.status_code == 400

    def test_retrieve_employee(self, auth_client):
        employee = EmployeeFactory()
        response = auth_client.get(f'/api/v1/employees/{employee.id}/')
        assert response.status_code == 200
        assert response.data['id'] == str(employee.id)

    def test_retrieve_employee_not_found(self, auth_client):
        import uuid
        response = auth_client.get(f'/api/v1/employees/{uuid.uuid4()}/')
        assert response.status_code == 404

    def test_update_employee(self, auth_client):
        employee = EmployeeFactory()
        data = {'first_name': 'Updated'}
        response = auth_client.put(f'/api/v1/employees/{employee.id}/', data, format='json')
        assert response.status_code == 200
        assert response.data['first_name'] == 'Updated'

    def test_partial_update_employee(self, auth_client):
        employee = EmployeeFactory()
        data = {'first_name': 'Patched'}
        response = auth_client.patch(f'/api/v1/employees/{employee.id}/', data, format='json')
        assert response.status_code == 200
        assert response.data['first_name'] == 'Patched'

    def test_delete_employee(self, auth_client):
        employee = EmployeeFactory()
        response = auth_client.delete(f'/api/v1/employees/{employee.id}/')
        assert response.status_code == 204
        employee.refresh_from_db()
        assert employee.is_active is False

    def test_search_employee(self, auth_client):
        EmployeeFactory(first_name='Diamant')
        response = auth_client.get('/api/v1/employees/?search=Diamant')
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_filter_by_department(self, auth_client):
        EmployeeFactory(department='IT')
        EmployeeFactory(department='HR')
        response = auth_client.get('/api/v1/employees/?department=IT')
        assert response.status_code == 200
        assert all(e['department'] == 'IT' for e in response.data)