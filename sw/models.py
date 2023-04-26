from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number=phone_number, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(max_length=10, unique=True)
    location = models.CharField(max_length=255, null=True)
    national_id = models.CharField(max_length=20, unique=True)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default="net.jpg")
    otp = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')
    occupation = models.CharField(max_length=50)

    def __str__(self):
        return self.user.full_name

class Worker(models.Model):
    SKILLS = (
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('carpenter', 'Carpenter'),
        # Add more skills as needed
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='worker')
    skill = models.CharField(max_length=50, choices=SKILLS)

    def __str__(self):
        return self.user.full_name


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_worker')
    service = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Booking #{self.id} - {self.service} on {self.date}'

