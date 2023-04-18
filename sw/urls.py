from django.urls import path
from .views import Endpoints, ClientSigninAPIView, WorkerSigninAPIView, VerifyOTP, ListClients, ListWorkers, Booking

urlpatterns = [
    path('', Endpoints.as_view()),
    path('client-signin/', ClientSigninAPIView.as_view()),
    path('worker-signin/', WorkerSigninAPIView.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),
    path('clients/', ListClients.as_view()),
    path('workers/', ListWorkers.as_view()),
    path('booking/', Booking.as_view()),
]
