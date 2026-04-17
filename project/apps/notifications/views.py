from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/index.html'
    login_url = 'users:login'
    redirect_field_name = 'next'

