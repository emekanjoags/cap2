from django.urls import path
from .views import TestimonyView

app_name = 'testimony'

urlpatterns = [
    path('', TestimonyView.as_view(), name='testimony')
]