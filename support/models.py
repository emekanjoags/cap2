from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ticket(models.Model):
   username = models.CharField(max_length=50, null=True, blank=True)
   subject = models.CharField(max_length=50, null=True, blank=True)
   text = models.CharField(max_length=1000, null=True, blank=True)
   image = models.ImageField(upload_to="uploads/support", blank=True, null=True)
   seen = models.IntegerField(default=0)
   date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
   def __str__(self):
       return self.username