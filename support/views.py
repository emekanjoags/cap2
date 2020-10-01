from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Ticket
from django.urls import reverse
from django.core import mail


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
        email = data.get('email')
        image = request.FILES.get('image')

        if subject and content and email:
            Ticket.objects.create(subject=subject, text=content, image=image, username=user)
            try:
                mail_subject = "New support ticket created"
                message = content
                from_mail = "support@leveragecapital.com.ng"
                to_mail = 'leveragecapitalng@gmail.com'
                mail.send_mail(mail_subject, message, from_mail, [to_mail])
            except Exception as e:
                print('error: ', e)
            messages.success(request, 'Ticket created successfully, we will get back to you within 24 hours')
            return HttpResponseRedirect(reverse('support:support'))
        messages.warning(request, 'Your ticket needs a subject, content and email, fill them in and submit again')
        return HttpResponseRedirect(reverse('support:support'))
    return render(request, 'support/ticket.html')
