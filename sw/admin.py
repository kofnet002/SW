from django.contrib import admin
from .models import Client, Worker, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Client)
admin.site.register(Worker)
