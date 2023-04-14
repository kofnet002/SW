from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from .serializers import UserSerializer, ClientSerializer
from .models import CustomUser, Client


class Endpoints(APIView):
    def get(self, request):
        endpoint = [
            "/signin"
        ]
        return Response(endpoint)


class ListClients(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class SigninAPIView(APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.save(commit=False)
            phone = name.phone_number
            name.save()

        # phone = request.data.get('phone')
        # user_type = request.data.get('user_type')

        # Check if the user is a client or a worker
        # if user_type not in ['client', 'worker']:
        #     return Response({'error': 'Invalid user type'})

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Save the OTP to the session
        # request.session['otp'] = otp
        # request.session['phone'] = phone
        # request.session['user_type'] = user_type

        # Send the OTP via Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )

        return Response({'success': True})


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
