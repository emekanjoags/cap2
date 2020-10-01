from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import Referral, WithrawRefBal
from authentication.models import Profile
from testimony.models import Testimony
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def homePage(request):
    content = Testimony.objects.all().order_by("-time")[:6]
    contex = {
        'content':content
    }
    return render(request, 'index.html', contex)

def faq(request):
    return render(request, 'faq.html')

@login_required(login_url='authentication:login-page')
def referral(request):
    profile = Profile.objects.get(user=request.user)
    referral = Referral.objects.filter(referrer=request.user)
    ref_code = profile.referral_code
    withdraw_btn = 0
    if profile.referred_active % 5 == 0 and profile.referral_balance != 0:
        withdraw_btn = 1

    if profile.referred_active == 0:
        withdraw_btn = 0
    if request.method == "POST":
        if profile.referred_active % 5 == 0 and profile.referral_balance != 0:
            ref_bal = profile.referral_balance
            WithrawRefBal.objects.create(user=request.user, balance=ref_bal)
            profile.referral_balance = 0
            profile.save()
            messages.success(request, 'Withdrawal successful, your referral bonus will be added to your next receiving amount')
            return HttpResponseRedirect(reverse('referral'))
        else:
            messages.warning(request, 'You cannot withdraw your balance yet')
            return HttpResponseRedirect(reverse('referral'))

    context = {
        'referral':referral,
        'profile':profile,
        'ref_code':ref_code,
        'withdraw_btn':withdraw_btn
    }
    return render(request, 'referral/referral.html', context)
def tos(request):
    return render(request, 'tos.html')