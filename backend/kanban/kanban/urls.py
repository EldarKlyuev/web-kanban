from django.contrib import admin
from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/signup/', UserSignUpView.as_view()),
    path('users/', UsersApiView.as_view()),
    path('users/<int:pk>/', UserPostView.as_view()),
    path('user/<str:token_verify>/verify/', UserVerifyEmailView.as_view()),
    path('user/auth/', UserAuthView.as_view()),
    path('user/resetpassword/', UserResetPasswordView.as_view()),
    path('user/forgotpassword/', UserForgotPasswordView.as_view()),
    path('users/complitesingup/', UserCompliteSignUpView.as_view()),
]
