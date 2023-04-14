from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Client, Worker, CustomUser

# User = get_user_model()
User = CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'age', 'gender', 'phone_number', 'location', 'national_id', 'profile_picture', 'password']
        # fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            age=validated_data['age'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            location=validated_data['location'],
            national_id=validated_data['national_id'],
            profile_picture=validated_data['profile_picture'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['id', 'user', 'occupation']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        client = Client.objects.create(user=user, occupation=validated_data['occupation'])
        return client


class WorkerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Worker
        fields = ['id', 'user', 'skill']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        worker = Worker.objects.create(user=user, skill=validated_data['skill'])
        return worker
