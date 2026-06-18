from rest_framework import serializers
from apps.employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_code', 'first_name', 'last_name',
            'full_name', 'email', 'phone_number', 'department',
            'position', 'date_joined', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    class Meta:
        model = Employee
        fields = [
            'employee_code', 'first_name', 'last_name', 'email',
            'phone_number', 'department', 'position',
            'date_joined', 'is_active'
        ]


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'department', 'position', 'date_joined', 'is_active'
        ]
        extra_kwargs = {field: {'required': False} for field in fields}