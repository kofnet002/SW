from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import Endpoints, ClientSigninAPIView, WorkerSigninAPIView, VerifyOTP, ListClients, ListWorkers, Authenticate, Booking


urlpatterns = [
    path('', Endpoints.as_view()),
    path('client-signup/', ClientSigninAPIView.as_view()),
    path('worker-signup/', WorkerSigninAPIView.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),
    path('clients/', ListClients.as_view()),
    path('workers/', ListWorkers.as_view()),
    path('booking/', Booking.as_view()),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', Authenticate.as_view(), name='login'),
]
