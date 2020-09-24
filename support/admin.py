from django.contrib import admin
from .models import Ticket
# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ('username', 'subject', 'date', 'seen')
    ordering = ('-date',)
    list_filter = ('seen',)
    search = ('subject',)

admin.site.register(Ticket, TicketAdmin)
