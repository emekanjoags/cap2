from django.contrib import admin
from .models import *


class ReceiversAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'amount', 'has_received', 'receiving_type', 'enter_list', 'has_entered_list', 'has_testified', 'date_entered'
    )
    list_filter = ('receiving_type', 'has_entered_list', 'date_entered', 'has_testified', 'has_received', 'enter_list')
    search_fields = ('user', 'amount')
    filter_horizontal = ()
    ordering = ('date_entered',)

class ReservedReceiversAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'receiving_amount', 'receiving_user', 'transaction_type', 'date_reserved', 'have_paid', 'have_received', 'blocked'
    )
    list_filter = ('date_reserved', 'have_paid', 'blocked',)
    search_fields = ('user', 'receiving_user',)
    filter_horizontal = ()
    ordering = ('receiving_amount',)
class AmountDonatedAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'completed', 'receiver_created')
    list_filter = ('completed', 'receiver_created',)
    filter_horizontal = ()
    ordering = ('amount',)

class InvestorAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'package', 'amount', 'matched', 'invested_amt')
    
admin.site.register(Receivers, ReceiversAdmin)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(ReceiversList)
admin.site.register(ReservedReceivers, ReservedReceiversAdmin)
admin.site.register(PayerRemnant)
admin.site.register(AmountDonated, AmountDonatedAdmin)
admin.site.register(Timer)