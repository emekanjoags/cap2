from django.shortcuts import render
from django.views.generic.base import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Testimony
from authentication.models import Profile

class TestimonyView(View):
    def get(self, request):
        content = Testimony.objects.all().order_by('-id')
        paginator = Paginator(content, 7)
        page = request.GET.get('page')

        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        context = {
            'post_list':post_list,
            'page':page
        }
        return render(request, 'testimony.html', context)
