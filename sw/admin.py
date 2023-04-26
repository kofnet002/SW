from django.contrib import admin
from .models import Client, Worker, CustomUser, Booking

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Client)
admin.site.register(Worker)
admin.site.register(Booking)
