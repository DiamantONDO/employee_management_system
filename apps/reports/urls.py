from django.urls import path
from apps.reports.views import EmployeeSummaryView, DepartmentSummaryView

urlpatterns = [
    path('reports/employee-summary/', EmployeeSummaryView.as_view(), name='employee-summary'),
    path('reports/department-summary/', DepartmentSummaryView.as_view(), name='department-summary'),
]