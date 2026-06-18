import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.attendance.tests.factories import AttendanceFactory
from apps.employees.tests.factories import EmployeeFactory
from django.contrib.auth.models import User
from datetime import date


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
class TestAttendanceViews:

    def test_list_attendance_unauthenticated(self, api_client):
        response = api_client.get('/api/v1/attendances/')
        assert response.status_code == 401

    def test_list_attendance_authenticated(self, auth_client):
        AttendanceFactory.create_batch(3)
        response = auth_client.get('/api/v1/attendances/')
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_attendance(self, auth_client):
        employee = EmployeeFactory()
        data = {
            'employee': str(employee.id),
            'attendance_date': str(date.today()),
            'check_in_time': '09:00:00',
            'check_out_time': '17:00:00',
            'status': 'PRESENT',
        }
        response = auth_client.post('/api/v1/attendances/', data, format='json')
        assert response.status_code == 201

    def test_create_attendance_duplicate(self, auth_client):
        attendance = AttendanceFactory()
        data = {
            'employee': str(attendance.employee.id),
            'attendance_date': str(attendance.attendance_date),
            'status': 'PRESENT',
        }
        response = auth_client.post('/api/v1/attendances/', data, format='json')
        assert response.status_code == 400

    def test_retrieve_attendance(self, auth_client):
        attendance = AttendanceFactory()
        response = auth_client.get(f'/api/v1/attendances/{attendance.id}/')
        assert response.status_code == 200
        assert response.data['id'] == str(attendance.id)

    def test_update_attendance(self, auth_client):
        attendance = AttendanceFactory()
        data = {'status': 'ABSENT'}
        response = auth_client.put(f'/api/v1/attendances/{attendance.id}/', data, format='json')
        print(response.data)  # add this
        assert response.status_code == 200
        assert response.data['status'] == 'ABSENT'

    def test_partial_update_attendance(self, auth_client):
        attendance = AttendanceFactory()
        data = {'status': 'ABSENT'}
        response = auth_client.patch(f'/api/v1/attendances/{attendance.id}/', data, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'ABSENT'

    def test_delete_attendance(self, auth_client):
        attendance = AttendanceFactory()
        response = auth_client.delete(f'/api/v1/attendances/{attendance.id}/')
        assert response.status_code == 204

    def test_filter_by_status(self, auth_client):
        AttendanceFactory(status='PRESENT')
        AttendanceFactory(status='ABSENT')
        response = auth_client.get('/api/v1/attendances/?status=PRESENT')
        assert response.status_code == 200
        assert all(a['status'] == 'PRESENT' for a in response.data)

    def test_filter_by_employee(self, auth_client):
        employee = EmployeeFactory()
        AttendanceFactory(employee=employee)
        response = auth_client.get(f'/api/v1/attendances/?employee_id={employee.id}')
        assert response.status_code == 200
        assert len(response.data) >= 1