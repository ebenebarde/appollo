from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet

# Binding the ViewSet explicitely to the 'create' action for the register endpoint
register_view = UserViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('register/', register_view, name='auth_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]