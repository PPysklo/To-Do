from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy


# Create your views here.

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks:tasks')
    
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks:tasks')    
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        
        return super(UserRegisterView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks:tasks')
    
        return super(UserRegisterView, self).get(*args, **kwargs)
    