from django.contrib import admin
from .models import Testimony

class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('user', 'time')
    search_fields = ('user',)
    ordering = ('-time',)

admin.site.register(Testimony, TestimonyAdmin)
