from rest_framework import serializers
from apps.attendance.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source='employee.full_name', read_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'attendance_date',
            'check_in_time', 'check_out_time', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'employee', 'attendance_date', 'check_in_time',
            'check_out_time', 'status'
        ]


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    check_in_time = serializers.TimeField(required=False, allow_null=True)
    check_out_time = serializers.TimeField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=Attendance.STATUS_CHOICES,
        required=False
    )

    class Meta:
        model = Attendance
        fields = ['check_in_time', 'check_out_time', 'status']