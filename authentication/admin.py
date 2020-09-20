from django.contrib import admin

# Register your models here.
from .models import Profile, BlockedUser
admin.site.register(Profile)
admin.site.register(BlockedUser)