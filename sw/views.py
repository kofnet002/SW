from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from .serializers import UserSerializer, ClientSerializer, WorkerSerializer
from .models import CustomUser, Client, Worker
import random


class Endpoints(APIView):
    def get(self, request):
        endpoint = [
            "/client-signin",
            "/worker-signin",
            "/clients",
            "/workers",
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
            obj = serializer.save(commit=False)

            phone = serializer.data.get("user").get("phone_number")

            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Send the OTP via Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP is: {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )

            serializer.data.get("user").update({"otp":otp})
            
            thisdict.update({"color": "red"})

            _otp = serializer.data.g
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class WorkerSigninAPIView(APIView):
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("Phone number:", serializer.data.get("user").get("phone_number"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPIView(APIView):
    def post(self, request):
        otp = request.data.get('otp')

        # Check if OTP matches the one saved in the session
        if str(otp) == str(request.session.get('otp')):
            phone = request.session.get('phone')
            user_type = request.session.get('user_type')

            # Authenticate the user based on user_type
            user = authenticate(request, phone=phone, user_type=user_type)

            if user is not None:
                # Log the user in and return a success response
                login(request, user)
                return Response({'success': True})
            else:
                return Response({'error': 'Invalid credentials'}, status=401)
        else:
            return Response({'error': 'Invalid OTP'}, status=400)
