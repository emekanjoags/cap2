from django.db import models
from django.contrib.auth.models import User
from authentication.models import Profile

# Create your models here.
class ReservedReceivers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='giver', null=True, blank=True)
    donation_amount = models.IntegerField(null=True, blank=True)
    receiving_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
    receiving_amount = models.FloatField(null=True, blank=True)
    transaction_type = models.IntegerField(null=True, blank=True)
    date_reserved = models.DateTimeField(auto_now_add=True)
    have_paid = models.BooleanField(default=False)#becomes True when user uploads proof of payment
    have_received = models.BooleanField(default=False)#becomes true when reciver confirms
    phone = models.CharField( max_length=20, blank=True, null=True)
    givers_phone = models.CharField( max_length=20, blank=True, null=True)
    receivers_name = models.CharField( max_length=200, blank=True, null=True)
    givers_name = models.CharField( max_length=200, blank=True, null=True)
    account_name = models.CharField(max_length=300, blank=True, null=True)
    account_number= models.CharField(max_length=300, blank=True, null=True)
    bank = models.CharField(max_length=300, blank=True, null=True)
    bitcoin_wallet = models.CharField(max_length=300, blank=True, null=True)
    pop = models.ImageField(upload_to="uploads/pop", blank=True, null=True)
    expiry_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    blocked = models.BooleanField(default=False)
    def __str__(self):
        return "{} will pay {} - {}".format(self.user.username, self.receiving_user, self.date_reserved)
    
    class Meta:
        verbose_name_plural = 'Reserved Receivers'

class Receivers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_mod = models.IntegerField(default=0)
    name = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    receiving_type = models.IntegerField(null=True, blank=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    date_start = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    has_received = models.BooleanField(default=False)
    enter_list = models.BooleanField(default=False)
    has_entered_list = models.BooleanField(default=False, null=True, blank=True)
    blocked = models.BooleanField(default=False)
    display_msg = models.BooleanField(default=True)
    has_testified = models.BooleanField(default=False)


    def __str__(self):
        return "{} - {} - {} - enter_list {}- has received {}".format(self.user, self.amount, self.date_entered, self.enter_list, self.has_received)         # return self.user.username
    class Meta:
        verbose_name_plural = 'Receivers'

class ReceiversList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    receiving_type = models.IntegerField(null=True, blank=True)
    date_entered = models.DateTimeField(auto_now_add=True)

class PayerRemnant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    has_remnant = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class AmountDonated(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False) #this will be true when the reeciver ticks that he has been paid
    receiver_created = models.BooleanField(default=False)

    def __str__(self):
        return '{} - has paid - {}'.format(self.user.username, self.completed)
    class Meta:
        verbose_name_plural = 'Amount Donated'

class Timer(models.Model):
    list_appear = models.DateTimeField(auto_now_add=False)
    list_disappear = models.DateTimeField(auto_now_add=False)
    text = models.CharField(max_length=300, blank=True, null=True)
    list_next_time = models.DateTimeField(auto_now_add=False, null=True)
    def __str__(self):
        return 'last _disappear time  is {}'.format(self.list_disappear)
    class Meta:
        verbose_name_plural = 'Timer'