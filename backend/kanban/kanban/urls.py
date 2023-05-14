from django.contrib import admin
from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/user/signup/', UserSignUpView.as_view()),
    path('api/v1/users/', UsersApiView.as_view()),
    path('api/v1/users/<int:pk>/', UserPostView.as_view()),
    path('api/v1/user/<str:token_verify>/verify/', UserVerifyEmailView.as_view()),
    path('api/v1/user/auth/', UserAuthView.as_view()),
    path('api/v1/user/resetpassword/', UserResetPasswordView.as_view()),
    path('api/v1/user/forgotpassword/', UserForgotPasswordView.as_view()),
    path('api/v1/users/complitesingup/', UserCompliteSignUpView.as_view()),

    path('api/v1/task/create/', TaskCreateView.as_view()),
    path('api/v1/task/<int:pk>/', TaskGPDView.as_view()),
]
