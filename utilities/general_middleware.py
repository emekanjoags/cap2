from django.http import HttpResponseRedirect
from django.urls import reverse


class AuthCheckMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return None
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/')


class AuthCheckLoginMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return None
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect(reverse('authentication:login-page'))

class AdminCheckMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return HttpResponseRedirect('/')
            else:
                return None
        else:
            return HttpResponseRedirect('/')
