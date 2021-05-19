from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from backend_test.utils.secure import user_has_permissions

class MultiSerializerViewSetMixin:
    """
    Mixin to allow the Viewset to use multiple serializers

    Note
    -----
    It is necessary to instantiate the variable 'serializers list' with
    at least one value 'default'
    
    serializers_list = {
        "default': ExampleSerializer(),
    }
    """

    def get_serializer_class(self):
        # Bring the serializer that the action needs
        if self.action in self.serializers_list:
            return self.serializers_list.get(self.action)
        return self.serializers_list.get("default")

class SecureModelViewSet(viewsets.ModelViewSet):
    """
    Viewset configuration with greater security, when inheriting from
    this function everything should continue working without implementing
    any adjustments
    """
    def __init__(self, **kwargs):
        app_label, model_name = self.model._meta.label.lower().split(".")

        # Implement a default permission setting to the Viewset
        self.permissions_list = {
            **{
                "default": ["%s.view_%s" % (app_label, model_name)],
                "create": ["%s.add_%s" % (app_label, model_name)],
                "list": ["%s.view_%s" % (app_label, model_name)],
                "retrieve": ["%s.view_%s" % (app_label, model_name)],
                "update": ["%s.change_%s" % (app_label, model_name)],
                "partial_update": ["%s.change_%s" % (app_label, model_name)],
                "destroy": ["%s.delete_%s" % (app_label, model_name)],
            },
            # Merge the default permissions to the custom ones in the Viewset
            **getattr(self, "permissions_list", {})
        }

        """
        By default all the actions of the Viewset will have the restriction
        of authenticated user
        """
        self.access_list = {
            **{
                "default": [IsAuthenticated],
            },
            # Merge the default access to the custom ones in the Viewset
            **getattr(self, "access_list", {})
        }

        super(SecureModelViewSet, self).__init__(**kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this
        view requires
        """
        if self.action in self.access_list:
            permission_classes = self.access_list.get(self.action)
        else:
            permission_classes = self.access_list.get("default")

        return [permission() for permission in permission_classes]

    def check_permissions(self, request):
        """
        Validate that the user has the necessary permissions
        """
        required_permissions = self.permissions_list.get(
            self.action,
            self.permissions_list.get("default")
        )

        if required_permissions and not user_has_permissions(
            request.user,
            required_permissions
        ):
            self.permission_denied(
                request, message=getattr(
                    None,
                    "message",
                    "You do not have the necessary permissions to perform this action"
                )
            )

        super(SecureModelViewSet, self).check_permissions(request)

class SecureMultiSerializerModelViewSet(
    MultiSerializerViewSetMixin,
    SecureModelViewSet
):
    """
    Create a class with security enhancements for the ModelViewSet
    including multiple serializer functionality
    """
    pass