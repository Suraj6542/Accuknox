# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterAPIView, CustomAuthToken, UserSearchAPIView, FriendRequestViewSet

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-requests')

urlpatterns = [
     path('register/', RegisterAPIView.as_view(), name='register'),
    path('users/register/', RegisterAPIView.as_view(), name='user-register'),
    path('users/login/', CustomAuthToken.as_view(), name='user-login'),
    path('users/search/', UserSearchAPIView.as_view(), name='user-search'),
    path('', include(router.urls)),
]
