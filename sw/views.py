from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from .serializers import UserSerializer, ClientSerializer, WorkerSerializer, ServiceSerializer,  BookSerializer, VerifyOTPSerializer
from .models import CustomUser, Client, Worker, Service, Book
import random
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.contrib.auth.models import Group


class Endpoints(APIView):
    def get(self, request):
        endpoint = [
            "/client-register",
            "/worker-register",
            "/token/",  # login
            "/clients",
            "/workers",
            "/verify-otp",
            "/services",
            "/book"
        ]
        return Response(endpoint)


# =========================== CLIENT VIEWS =========================
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
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'detail': 'OTP verified successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = Service.objects.all()
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        task = request.data.get('task')

        data = {
            "user":  user.id,
            "task": task
        }
        serializer = BookSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Book.objects.all()
        serializer = BookSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        task = request.data.get('task')

        data = {
            'user': user.id,
            'task': task
        }


        serializer = BookSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================== WORKER VIEWS =========================
class GetBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Book.objects.all()
        serializer = BookSerializer(bookings, many=True)
        _all = [d.get('user') for d in serializer.data]
        print(_all)
        return Response(serializer.data, status=status.HTTP_200_OK)
