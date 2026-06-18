from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.attendance.services import AttendanceService
from apps.attendance.serializers import (
    AttendanceSerializer,
    AttendanceCreateSerializer,
    AttendanceUpdateSerializer
)


class AttendanceViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AttendanceService()

    @extend_schema(
        summary="List all attendance records",
        parameters=[
            OpenApiParameter("employee_id", str, description="Filter by employee"),
            OpenApiParameter("status", str, description="Filter by status"),
            OpenApiParameter("date", str, description="Filter by date"),
            OpenApiParameter("start_date", str, description="Filter by start date"),
            OpenApiParameter("end_date", str, description="Filter by end date"),
        ],
        responses={200: AttendanceSerializer(many=True)},
        tags=["Attendance"]
    )
    def list(self, request):
        employee_id = request.query_params.get('employee_id')
        status_param = request.query_params.get('status')
        date_param = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if employee_id:
            records = self.service.get_employee_attendance(employee_id)
        elif start_date and end_date:
            records = self.service.get_attendance_by_date_range(start_date, end_date)
        else:
            filters = {}
            if status_param:
                filters['status'] = status_param
            if date_param:
                filters['attendance_date'] = date_param
            records = self.service.get_all_attendance(filters)

        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve an attendance record",
        responses={200: AttendanceSerializer},
        tags=["Attendance"]
    )
    def retrieve(self, request, pk=None):
        try:
            attendance = self.service.get_attendance_by_id(pk)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    @extend_schema(
        summary="Create an attendance record",
        request=AttendanceCreateSerializer,
        responses={201: AttendanceSerializer},
        tags=["Attendance"]
    )
    def create(self, request):
        serializer = AttendanceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            attendance = self.service.create_attendance(serializer.validated_data)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update an attendance record",
        request=AttendanceUpdateSerializer,
        responses={200: AttendanceSerializer},
        tags=["Attendance"]
    )
    def update(self, request, pk=None):
        serializer = AttendanceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            attendance = self.service.update_attendance(pk, serializer.validated_data)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(AttendanceSerializer(attendance).data)

    @extend_schema(
        summary="Partially update an attendance record",
        request=AttendanceUpdateSerializer,
        responses={200: AttendanceSerializer},
        tags=["Attendance"]
    )
    def partial_update(self, request, pk=None):
        serializer = AttendanceUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            attendance = self.service.update_attendance(pk, serializer.validated_data)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(AttendanceSerializer(attendance).data)

    @extend_schema(
        summary="Delete an attendance record",
        responses={204: None},
        tags=["Attendance"]
    )
    def destroy(self, request, pk=None):
        try:
            self.service.delete_attendance(pk)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)