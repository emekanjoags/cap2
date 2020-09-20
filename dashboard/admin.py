from django.contrib import admin
from .models import *

admin.site.register(Receivers)
admin.site.register(ReceiversList)
admin.site.register(ReservedReceivers)
admin.site.register(PayerRemnant)
admin.site.register(AmountDonated)