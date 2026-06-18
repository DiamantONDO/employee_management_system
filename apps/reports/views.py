from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.reports.services import ReportService


class EmployeeSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get employee attendance summary",
        parameters=[
            OpenApiParameter("employee_id", str, required=True),
            OpenApiParameter("start_date", str, required=True),
            OpenApiParameter("end_date", str, required=True),
        ],
        tags=["Reports"]
    )
    def get(self, request):
        employee_id = request.query_params.get('employee_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not all([employee_id, start_date, end_date]):
            return Response(
                {"detail": "employee_id, start_date and end_date are required."},
                status=400
            )
        try:
            summary = ReportService().get_employee_summary(employee_id, start_date, end_date)
        except ValidationError as e:
            return Response(e.message_dict, status=404)
        return Response(summary)


class DepartmentSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get department attendance summary",
        parameters=[
            OpenApiParameter("department", str, required=True),
            OpenApiParameter("start_date", str, required=True),
            OpenApiParameter("end_date", str, required=True),
        ],
        tags=["Reports"]
    )
    def get(self, request):
        department = request.query_params.get('department')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not all([department, start_date, end_date]):
            return Response(
                {"detail": "department, start_date and end_date are required."},
                status=400
            )
        summary = ReportService().get_department_summary(department, start_date, end_date)
        return Response(summary)