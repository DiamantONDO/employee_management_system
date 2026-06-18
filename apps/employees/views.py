from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.employees.services import EmployeeService
from apps.employees.serializers import (
    EmployeeSerializer,
    EmployeeCreateSerializer,
    EmployeeUpdateSerializer
)


class EmployeeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = EmployeeService()

    @extend_schema(
        summary="List all employees",
        parameters=[
            OpenApiParameter("search", str, description="Search by name"),
            OpenApiParameter("department", str, description="Filter by department"),
            OpenApiParameter("is_active", bool, description="Filter by active status"),
        ],
        responses={200: EmployeeSerializer(many=True)},
        tags=["Employees"]
    )
    def list(self, request):
        search = request.query_params.get('search')
        department = request.query_params.get('department')
        is_active = request.query_params.get('is_active')

        if search:
            employees = self.service.search_employees(search)
        elif department or is_active is not None:
            is_active_bool = None
            if is_active is not None:
                is_active_bool = is_active.lower() == 'true'
            employees = self.service.filter_employees(
                department=department,
                is_active=is_active_bool
            )
        else:
            employees = self.service.get_all_employees()

        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve an employee",
        responses={200: EmployeeSerializer},
        tags=["Employees"]
    )
    def retrieve(self, request, pk=None):
        try:
            employee = self.service.get_employee_by_id(pk)
        except ValidationError as e:
            return Response({"detail": e.messages[0]}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    @extend_schema(
        summary="Create an employee",
        request=EmployeeCreateSerializer,
        responses={201: EmployeeSerializer},
        tags=["Employees"]
    )
    def create(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            employee = self.service.create_employee(serializer.validated_data)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update an employee",
        request=EmployeeUpdateSerializer,
        responses={200: EmployeeSerializer},
        tags=["Employees"]
    )
    def update(self, request, pk=None):
        serializer = EmployeeUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            employee = self.service.update_employee(pk, serializer.validated_data)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(EmployeeSerializer(employee).data)

    @extend_schema(
        summary="Partially update an employee",
        request=EmployeeUpdateSerializer,
        responses={200: EmployeeSerializer},
        tags=["Employees"]
    )
    def partial_update(self, request, pk=None):
        serializer = EmployeeUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            employee = self.service.update_employee(pk, serializer.validated_data)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(EmployeeSerializer(employee).data)

    @extend_schema(
        summary="Soft delete an employee",
        responses={204: None},
        tags=["Employees"]
    )
    def destroy(self, request, pk=None):
        try:
            self.service.delete_employee(pk)
        except ValidationError as e:
            return Response({"detail": e.messages[0]}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)