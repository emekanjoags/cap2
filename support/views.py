from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Ticket
from django.urls import reverse

# Create your views here.

def support(request):
    context = {}
    if request.method == "POST":
        data = request.POST
        user = 'anonymous'
        if request.user.is_authenticated:
            user = request.user.username
    
        subject = data.get('subject')
        content = data.get('content')
        image = request.FILES.get('image')

        if subject and content:
            Ticket.objects.create(subject=subject, text=content, image=image, username=user)
            messages.success(request, 'Ticket created successfully, we will get back to you within 24 hours')
            return HttpResponseRedirect(reverse('support:support'))
        messages.warning(request, 'Your ticket needs a subject and content, fill them in and submit again')
        return HttpResponseRedirect(reverse('support:support'))
    return render(request, 'support/ticket.html')
