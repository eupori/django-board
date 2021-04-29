#-*- coding: utf-8 -*-
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = 'home.html'


class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('register_done')


class UserCreateDoneTemplateView(TemplateView):
    template_name = 'registration/gegister_done.html'

