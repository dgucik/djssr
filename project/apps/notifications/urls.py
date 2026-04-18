from apps.notifications.views import NotificationsView, SendNotificationView
from django.urls import path

from apps.notifications.senders.sms import SmsSender
from apps.notifications.services.notification import NotificationService

app_name = 'notifications'

urlpatterns = [
    path('', NotificationsView.as_view(), name='index'),
    path('send/', SendNotificationView.as_view(), name='send'),
]