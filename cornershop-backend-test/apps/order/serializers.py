from datetime import datetime
from rest_framework import serializers
from apps.menu.serializers import MenuDetailSerializer
from apps.employee.serializers import EmployeeSerializer
from apps.menu.serializers import DishSerializer
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for any action that involves creating or modifying an order
    """
    class Meta:
        model = Order
        fields = (
            "id",
            "dishes",
            "note",
        )

    def validate(self, data):
        # Only orders that are being modified are validated
        if self.instance:
            menu_object = self.instance.menu
            datetime_limit = datetime.combine(
                menu_object.date,
                menu_object.time_limit
            )

            # It is validated that there is still time to place the order
            if datetime.now() > datetime_limit:
                raise serializers.ValidationError({
                    "detail": "The deadline to place the order has expired"
                })

        return data

class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for list type actions

    Note
    ------
    The menu information is not shown because it must be filtered as a
    parament in the url
    """
    employee = EmployeeSerializer()
    dishes = DishSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "employee",
            "dishes",
            "note",
            "created",
            "modified",
        )

class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detail type actions

    Note
    ------
    Since the information of the menu and the possible dishes is shown, this
    serializer will only report the ids of the dishes chosen by the employee
    in the variable "dishes"
    """
    menu = MenuDetailSerializer()
    employee = EmployeeSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "menu",
            "employee",
            "dishes",
            "note",
            "created",
            "modified",
        )