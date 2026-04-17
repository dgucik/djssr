from apps.notifications.views import NotificationsView
from django.urls import path

app_name = 'notifications'

urlpatterns = [
    path('', NotificationsView.as_view(), name='index'),
]