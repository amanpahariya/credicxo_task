from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from api.views import *


router = routers.DefaultRouter()
router.register(r'register/teacher', RegisterTeacherViewSet,basename="teacher")
router.register(r'register/student', RegisterStudentViewSet,basename="student")
router.register(r'users', UserDetailsViewSet,basename="users")


urlpatterns = [
    # login url
    path('',include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # update refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgotpassword/',ForgotPasswordViewSet.as_view(),name='forgot_password'),
    path('resetpassword/',ResetPasswordViewSet.as_view(),name='reset_password'),
]