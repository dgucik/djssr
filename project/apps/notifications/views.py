from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from apps.notifications.services import NotificationService
from apps.notifications.senders import get_sender

# Create your views here.
class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/index.html'
    login_url = 'users:login'
    redirect_field_name = 'next'


"""
Conventions:
W zaleznosci od tego czy wybór strategii ma byc dynamiczny czy statyczny, można zdecydować się na różne podejścia do implementacji widoku:
1. Dynamiczny wybór strategii:
   - W tym przypadku, widok może przyjmować parametr (np. z POST lub GET), który określa, która strategia ma być użyta. Na podstawie tego parametru, można dynamicznie tworzyć instancję odpowiedniego nadawcy (np. SmsSender, EmailSender) i przekazywać ją do serwisu powiadomień.
2. Statyczny wybór strategii:
    - uzywamy urls.py jako composition root, w którym wybieramy strategie i przekazujemy je do widoku. W tym przypadku, widok jest bardziej statyczny i nie musi się martwić o wybór strategii, ponieważ jest ona już ustalona w momencie tworzenia widoku.
"""
class SendNotificationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        message = request.POST.get('message', '')
        sender_type = request.POST.get('sender', '')

        sender = get_sender(sender_type)
        notification_service = NotificationService(sender)
        notification_service(user_id, message)

        return redirect('notifications:index')
    
