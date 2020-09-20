from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .form import UserCreateForm, ProfileForm, LostPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from account.models import Referral
from .models import Profile
from django.contrib.auth.models import User


# Create your views here.
def registration(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                used_email = User.objects.get(email=email)
                if used_email:
                    messages.warning(request, 'A user with this email {} already exist'.format(email))
                    return HttpResponseRedirect(reverse('authentication:registration'))
            except User.DoesNotExist:
                pass

            ref_code = form.cleaned_data['referral_code']
            if ref_code:
                try:
                    referrer = Profile.objects.get(referral_code=ref_code.lower())
                except Profile.DoesNotExist:
                    messages.warning(request, 'We do not have a user with this referral code - ' + ref_code)
                    return HttpResponseRedirect(reverse('authentication:registration'))
            user = form.cleaned_data.get('username')
            form.save()
            messages.success(request, 'account successfully created for ' + user)
            return HttpResponseRedirect(reverse('authentication:login-page'))
        # else:
        #     messages.warning(request, 'form not valid')
        #     return HttpResponseRedirect(reverse('authentication:registration'))
    context = {
        'form':form
    }
    return render(request, 'auth/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect ('/admin')
            else:
                messages.success(request, 'Welcome ' + username)
                return redirect('/')
        else:
            messages.warning(request, 'username or password incorrect')
            return HttpResponseRedirect(reverse('authentication:login-page'))
    return render(request, 'auth/login.html')

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login-page'))

class PasswordLost(View):
    form = LostPasswordForm
    def get(self, request):
        return render(request, 'auth/password/lost.html', {'form':self.form})

    def post(self, request):
        self.form = self.form(request.POST)
        if self.form.is_valid():
            try:
                user = User.objects.get(email=self.form.cleaned_data.get('email'))
            except User.DoesNotExist:
                messages.warning(request, ' A user with this e-mail does not exist')
                return HttpResponseRedirect(reverse('authentication:lost'))
            password_reset_link(request, user)
            messages.success(request, 'Password reset link has been sent to your email address. ')
        return render(request, 'auth/password/lost.html', {'form':self.form})