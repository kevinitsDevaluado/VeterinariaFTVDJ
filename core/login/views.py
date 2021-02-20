from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
#login formView
from django.views.generic import FormView, RedirectView
#AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
#reverse_lazy
from django.urls import reverse_lazy
#HttpResponseRedirect
from django.shortcuts import HttpResponseRedirect
#login -- logaut
from django.contrib.auth import login, logout 
#SETTINGS
import config.settings as setting
# Create your views here.

class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Iniciar Sesion'
        return context

class LoginFormView2(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    def dispatch(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tittle'] = 'Iniciar Sesion'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)