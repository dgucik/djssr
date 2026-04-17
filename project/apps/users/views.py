from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy

from apps.users.forms import RegistrationForm


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

