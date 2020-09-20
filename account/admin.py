from django.contrib import admin
from .models import Referral, ExchangeRate, WithrawRefBal

admin.site.register(Referral)
admin.site.register(ExchangeRate)
admin.site.register(WithrawRefBal)