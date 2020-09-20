from django.db import models
from django.contrib.auth.models import User
from authentication.models import Profile


class Testimony(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Testimonies'