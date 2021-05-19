from collections import OrderedDict
from rest_framework.fields import ChoiceField

class DetailChoiceField(ChoiceField):
    def to_representation(self, obj):
        """
        Used while retrieving value for the field.
        """
        return {
            "id": obj,
            "name": self._get_choices()[obj],
        }