from django.urls import path
from django.utils.decorators import decorator_from_middleware
from utilities.general_middleware import AuthCheckMiddleware, AuthCheckLoginMiddleware, AdminCheckMiddleware
from .views import ProfileDisplay, match
from dashboard.views import MatchApi, MakeDonation, MatchApib, MakeDonationB

user_auth_decorator = decorator_from_middleware(AuthCheckLoginMiddleware)
admin_auth_decorator = decorator_from_middleware(AdminCheckMiddleware)

app_name = "account"

urlpatterns = [
    path('', user_auth_decorator(ProfileDisplay.as_view()), name="profile"),
    path('admin-match', match, name='match'),
    path('api/investors', admin_auth_decorator(MatchApi.as_view())),
    path('api/investorsb', admin_auth_decorator(MatchApib.as_view())),
    path('api/match-bitcoin', admin_auth_decorator(MakeDonationB.as_view())),
    path('api/match-money', admin_auth_decorator(MakeDonation.as_view()))
]