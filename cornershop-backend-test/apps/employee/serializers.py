from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Generic serializer for employee structure
    """
    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "country",
            "slack_id",
        )