from django.contrib import admin
from django.urls import path, include
from core.homepage.views import IndexView
from core.login.views import LoginFormView,LoginFormView2, LogoutView, LogoutRedirectView
urlpatterns = [
    path('',LoginFormView.as_view(), name='login'), 
    #path('logout/',LogoutView.as_view(), name='logout'),
    path('logout/',LogoutRedirectView.as_view(), name='logout'),
]
