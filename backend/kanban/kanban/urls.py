from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from mainapp.views import *


schema_view = get_schema_view(
   openapi.Info(
      title="Med API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('api/v1/user/signup/', UserSignUpView.as_view()),
   path('api/v1/users/', UsersApiView.as_view()),
   path('api/v1/users/<int:pk>/', UserPostView.as_view()),
   path('api/v1/user/<str:token_verify>/verify/', UserVerifyEmailView.as_view()),
   path('api/v1/user/auth/', UserAuthView.as_view()),
   path('api/v1/user/auth/refresh_token/', UserAuthRefreshTokenView.as_view()),
   path('api/v1/user/resetpassword/', UserResetPasswordView.as_view()),
   path('api/v1/user/<str:token_reset>/forgotpassword/', UserForgotPasswordView.as_view()),
   path('api/v1/users/<str:token_complite_signup>/complitesingup/', UserCompliteSignUpView.as_view()),

   path('swagger(?P\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    
]
