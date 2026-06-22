from django.urls import path
from apps.reports.views import EmployeeSummaryView, DepartmentSummaryView, DepartmentSummaryExportView, \
    EmployeeSummaryExportView

urlpatterns = [
    path('reports/department-summary/export/', DepartmentSummaryExportView.as_view(), name='department-summary-export'),
    path('reports/employee-summary/export/', EmployeeSummaryExportView.as_view(), name='employee-summary-export'),
    path('reports/employee-summary/', EmployeeSummaryView.as_view(), name='employee-summary'),
    path('reports/department-summary/', DepartmentSummaryView.as_view(), name='department-summary'),
]