from django.urls import path
from .views import registration, logoutUser, PasswordLost
from django.contrib.auth import views as auth_views
app_name="authentication"

urlpatterns = [
    path('register', registration, name="registration"),
    # path('', loginPage, name='login-page'),
    path('logout', logoutUser, name='logout-user'),
    path('lost', PasswordLost.as_view(), name='lost'),

    
]