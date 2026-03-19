from django.contrib import admin
from .models import CustomUser,Bus,Driverprofile


# Register your models here.

admin.site.register(CustomUser)
admin.register(Bus)
admin.site.register(Driverprofile) 