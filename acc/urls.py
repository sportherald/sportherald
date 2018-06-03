from django.urls import path, re_path
from . import views

app_name='acc'

urlpatterns = [
    re_path('oauth/callback', views.handleCode.as_view(), name='oauth_callback'),
    ]