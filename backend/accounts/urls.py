from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet

register_view = UserViewSet.as_view({'post': 'create'})
user_detail_view = UserViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('register/', register_view, name='auth_register'),
    path('users/<slug:slug>/', user_detail_view, name='user_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
