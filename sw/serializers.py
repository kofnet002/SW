from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Client, Worker, CustomUser, Service, Book
import random
from .otp import MessageHandler


# User = get_user_model()
User = CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'age', 'gender', 'phone_number', 'location', 'national_id', 'otp', 'is_verified','profile_picture', 'password']
        extra_kwargs ={
            "password":{
                "write_only": True,
            }
        }
    # Generate 6 digits otp
    def generate_otp(self):
        """Generates a random six-digit OTP"""
        return str(random.randint(100000, 999999))

    def create(self, validated_data):
        
        # perform operation on validated_data
        otp = self.generate_otp()
        validated_data['otp'] = otp # Modify otp value

        user = User.objects.create(
            full_name=validated_data['full_name'],
            age=validated_data['age'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            location=validated_data['location'],
            national_id=validated_data['national_id'],
            otp=validated_data['otp'],
            # is_verified=validated_data['is_verified'],
            profile_picture=validated_data['profile_picture'],
        )

        # Send OTP to user
        messagehandler=MessageHandler(user.phone_number, otp).send_otp_via_message()

        user.set_password(validated_data['password'])
        user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Client
        # fields = ['id', 'user', 'occupation']
        fields = "__all__"
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        client = Client.objects.create(user=user, occupation=validated_data['occupation'])

        return client

class WorkerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Worker
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        worker = Worker.objects.create(user=user, skill=validated_data['skill'])
        return worker


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Book
        fields = "__all__"
        depth=1


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        # Check if the phone number exists in the database
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Phone number not found')

        # Check if the OTP matches
        if otp != str(user.otp):
            raise serializers.ValidationError('Incorrect OTP')

        # Update the is_verified field to True
        user.is_verified = True
        user.save()

        return data
