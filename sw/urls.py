from django.urls import path
from .views import Endpoints, SigninAPIView, VerifyOTPAPIView, ListClients

urlpatterns = [
    path('', Endpoints.as_view()),
    path('signin/', SigninAPIView.as_view()),
    path('verify-otp/', VerifyOTPAPIView.as_view()),
    path('clients/', ListClients.as_view()),
]
