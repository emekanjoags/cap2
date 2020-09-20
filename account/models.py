from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='referrer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='referrer_user')
    is_settled = models.BooleanField(default=False, blank=True, null=True)# this becomes active for the referrer as soon as the referre donates
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return "{} - {}".format(self.user.username, self.referrer.username)


class ExchangeRate(models.Model):
    rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return "Rate - {}".format(self.rate)

class WithrawRefBal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.IntegerField(default=0)
    collected = models.BooleanField(default=False)

    def __str__(self):
        return "{} - collected - {}".format(self.user.username, self.collected)