from django.urls import path
from django.utils.decorators import decorator_from_middleware
from utilities.general_middleware import AuthCheckMiddleware, AuthCheckLoginMiddleware
from .views import ProfileDisplay

user_auth_decorator = decorator_from_middleware(AuthCheckLoginMiddleware)

app_name = "account"

urlpatterns = [
    path('', user_auth_decorator(ProfileDisplay.as_view()), name="profile")
]