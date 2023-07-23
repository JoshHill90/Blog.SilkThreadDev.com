from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import RegForm, ProfileForm, UserIcon
from .models import Profile


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeView
    template_name = 'registration/change-password.html'
    success_url = reverse_lazy('index')



class UserEditView(generic.UpdateView):
    form_class = ProfileForm
    template_name = 'registration/edit-profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, *args):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        icon_id = form.cleaned_data['icon']
        user_profile = self.request.user.profile
        user_profile.icon = UserIcon.objects.get(name=icon_id)
        user_profile.save()
        return response

class UserRegistrationView(generic.CreateView):
    form_class = RegForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        return response