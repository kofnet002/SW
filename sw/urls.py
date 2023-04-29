from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


urlpatterns = [
    path('', Endpoints.as_view()),
    path('client-register/', ClientSigninAPIView.as_view()),
    path('worker-register/', WorkerSigninAPIView.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),
    path('clients/', ListClients.as_view()),
    path('workers/', ListWorkers.as_view()),
    path('services/', ServiceAPIView.as_view()),
    path('book/', BookAPIView.as_view()),

]
