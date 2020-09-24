from django.urls import path
from .views import support

app_name = 'support'

urlpatterns = [
    path('', support, name='support')
]