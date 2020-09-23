from django.contrib import admin

# Register your models here.
from .models import Profile, BlockedUser

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_referred', 'referral_balance', 'has_referred', 'referred_active', 'mode_of_receiving')
    list_filter = ('is_referred',)
    search = ('user', 'account_name')
    ordering = ('-referred_active',)
    filter_horizontal = ()
admin.site.register(Profile, ProfileAdmin)
admin.site.register(BlockedUser)