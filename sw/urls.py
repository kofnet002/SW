from django.urls import path
from .views import Endpoints, ClientSigninAPIView, WorkerSigninAPIView, VerifyOTPAPIView, ListClients, ListWorkers

urlpatterns = [
    path('', Endpoints.as_view()),
    path('client-signin/', ClientSigninAPIView.as_view()),
    path('worker-signin/', WorkerSigninAPIView.as_view()),
    path('verify-otp/', VerifyOTPAPIView.as_view()),
    path('clients/', ListClients.as_view()),
    path('workers/', ListWorkers.as_view()),
]
