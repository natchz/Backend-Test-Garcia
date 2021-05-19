from rest_framework import serializers
from backend_test.utils.serializers import DetailChoiceField
from backend_test.choices import DISH_TYPES
from .models import *

class DishSerializer(serializers.ModelSerializer):
    """
    Generic serializer for dishes

    Note
    ------
    DetailChoiceField returns a structure of {id, name}, it is used with
    variables that use choices
    """
    type = DetailChoiceField(choices=DISH_TYPES)

    class Meta:
        model = Dish
        fields = (
            "id",
            "name",
            "type",
        )

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer to list, create or modify menus
    """
    class Meta:
        model = Menu
        fields = (
            "id",
            "date",
            "country",
            "dishes",
            "time_limit",
            "published",
        )
        extra_kwargs = {
            "dishes": {"write_only": True},
        }

class MenuDetailSerializer(serializers.ModelSerializer):
    """
    Serializer bring detail information from a menu
    """
    dishes = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = (
            "id",
            "date",
            "country",
            "dishes",
            "time_limit",
            "published",
            "created",
            "modified",
        )