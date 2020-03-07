from django.urls import path
from rest_framework import routers

from .views import UserSignUpAPIView, UserViewSet, LoginAuthentication, \
    LogoutAuthentication

app_name = 'authentication'

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAuthentication.as_view(), name='login'),
    path('logout/', LogoutAuthentication.as_view(), name='logout'),
]

urlpatterns += router.urls
