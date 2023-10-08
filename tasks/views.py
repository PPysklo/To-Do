from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm
from .models import Task


# Create your views here.

class TaskList(LoginRequiredMixin, ListView):
    model = Task    
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        
        return context 
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    
    success_url = reverse_lazy('tasks:tasks')    

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(TaskCreate,self).form_valid(form)
        
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    
    success_url = reverse_lazy('tasks:tasks')    
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    
    success_url = reverse_lazy('tasks:tasks')    
    