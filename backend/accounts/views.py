from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer

# Get the custom user model
User = get_user_model()

class UserViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  viewsets.GenericViewSet):
    """
    ViewSet for User management.
    Handles:
    - Register (POST /api/v1/auth/register/) -> RegisterSerializer
    - Retrieve Profile (GET /api/v1/auth/users/{id}/) -> UserSerializer
    """
    queryset = User.objects.all()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - Create (Register): AllowAny
        - Retrieve (Profile): IsAuthenticated (or AllowAny depending on requirements)
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Return different serializers for different actions.
        """
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer