from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from .serializers import UserSerializer, ClientSerializer, WorkerSerializer, BookingSerializer
from .models import CustomUser, Client, Worker, Booking
import random
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.hashers import check_password



class Endpoints(APIView):
    def get(self, request):
        endpoint = [
            "/client-signin",
            "/worker-signin",
            "/clients",
            "/workers",
            "/verify-otp"
        ]
        return Response(endpoint)


class ListClients(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListWorkers(APIView):
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


# class VerifyOTP(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        # Query the database for the user with the specified phone number
        user = get_object_or_404(CustomUser, phone_number=phone_number)
        client_data = Client.objects.get(user=user)
        
        data = request.data.copy()
        print(user)
        data['user'] = request.user.pk

        serializer = ClientSerializer(instance=client_data, data=data)

        if serializer.is_valid():
            if otp == user.otp:
                serializer.validated_data['is_verified'] = True
                serializer.save(user=request.user) # set the user field

                # serializer.save()
                return Response("User is verified", status=status.HTTP_200_OK)
  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        # Query the database for the user with the specified phone number
        user = get_object_or_404(CustomUser, phone_number=phone_number)
        
        client_data = Client.objects.get(user=user)
        # print(client_data)
        # data = request.data.copy()
        # data['user'] = request.user.pk

        serializer = ClientSerializer(instance=user, data=user)
        

        if serializer.is_valid():
            print("Reached")
            if otp == user.otp:
                serializer.validated_data['is_verified'] = True
                
                serializer.save(user=request.user) # set the user field

                serializer.save()
                return Response("User is verified", status=status.HTTP_200_OK)
  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Authenticate(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = authenticate(request, phone_number=phone_number, password=password)
        
        print(user)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            # return Response({'error': 'Invalid credentials'}, status=400)
            return Response({'error': 'Invalid credentials'}, status=400)


class Booking(APIView):
    def get(self, request):
        req = "Client 1"
        bookings = Booking.objects.filter(user=req)
        _bookings = bookings.set_all(bookings)
        serializer = BookingSerializer(_bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)