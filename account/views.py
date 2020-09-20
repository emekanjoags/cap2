from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic.base import View
from django.contrib.auth.models import User
from authentication.models import Profile
from django.core import mail
# Create your views here.

class ProfileDisplay(View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        context = {
            "profile":profile
        }
        return render(request, 'account/profile.html', context)

    def post(self, request):
        phone = request.POST.get('phone')
        profile_pic = request.FILES.get('profile_image')
        account_num = request.POST.get('account_num')
        account_name = request.POST.get('account_name')
        bank = request.POST.get('bank')
        password = request.POST.get('password')
        bitcoin_wallet = request.POST.get('bitcoin_wallet')
        receiving_mode = request.POST.get('mode')
        retype_password = request.POST.get('retype_password')
        user = User.objects.get(id=request.user.pk)
        profile = Profile.objects.get(user=request.user)
        if phone:
            try:
                used_phone = Profile.objects.get(phone=phone)
                messages.warning(request, 'user with this number already exist')
                return HttpResponseRedirect(reverse('account:profile'))
            except Profile.DoesNotExist:                
                if len(phone) < 11:
                    messages.warning(request, 'please enter an accurate phone number')
                    return HttpResponseRedirect(reverse('account:profile'))
                profile.phone = phone
        if profile_pic:
            if profile_pic != profile.profile_pic:
                profile.profile_pic = profile_pic
        
        if account_num:
            profile.account_number = account_num
        if account_name:
            profile.account_name = account_name
        if bank:
            profile.bank = bank
        if receiving_mode == 'bitcoin':
            profile.mode_of_receiving = 2
        if bitcoin_wallet:
            profile.bitcoin_wallet = bitcoin_wallet
        if receiving_mode == 'naira':
            profile.mode_of_receiving = 1
        if password:
            if password == retype_password and len(password) >5:
                user.set_password(password)
                user.save()
            elif len(password) < 6:
                messages.warning(request, 'password should be at least 6 characters long')
                return HttpResponseRedirect(reverse('account:profile'))
            elif password != retype_password:
                messages.warning(request, 'password and retype password does not match')
                return HttpResponseRedirect(reverse('account:profile'))
            

        profile.save()
        messages.success(request, 'Profile updated successfully')
        return HttpResponseRedirect(reverse('account:profile'))


