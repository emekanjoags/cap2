from django.contrib.auth.models import User
from django import forms
from account.models import Referral
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserCreateForm(UserCreationForm):
    referral_code = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'referral_code', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        referral_code = self.cleaned_data['referral_code']
    
        if commit:
            user.save()
            user.refresh_from_db()
            if referral_code:
                try:
                    referrer = Profile.objects.get(referral_code=referral_code.lower())
                    Referral.objects.create(user=user, referrer=referrer.user)
                    profile = Profile.objects.get(user=user)
                    profile.is_referred = True
                    referrer.has_referred += 1
                    profile.save()
                    referrer.save()
                except Profile.DoesNotExist:
                    pass
        return user

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

class LostPasswordForm(forms.Form):
    email = forms.CharField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Please enter your email address.")

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("User with this e-mail address does not exist.")

        return cleaned_data