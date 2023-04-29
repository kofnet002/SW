from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from .serializers import UserSerializer, ClientSerializer, WorkerSerializer, ServiceSerializer
from .models import CustomUser, Client, Worker, Service
import random
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated




class Endpoints(APIView):
    def get(self, request):
        endpoint = [
            "/client-register",
            "/worker-register",
            "/token/", # login
            "/clients",
            "/workers",
            "/verify-otp",
            "/services"
        ]
        return Response(endpoint)


class ListClients(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListWorkers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ClientSigninAPIView(APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class WorkerSigninAPIView(APIView):
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        # Query the database for the user with the specified phone number
        user = get_object_or_404(CustomUser, phone_number=phone_number)

        data = request.data.copy()

        serializer = ClientSerializer(instance=user, data=data)

        if serializer.is_valid():
            if otp == user.otp:
                serializer.validated_data['is_verified'] = True
                serializer.save(user=request.user) # set the user field
                serializer.save()
                return Response("User is verified", status=status.HTTP_200_OK)
  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = Service.objects.all()
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        task = request.data.get('task')


        return Response("testing", status=status.HTTP_200_OK)