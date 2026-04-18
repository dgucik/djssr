from apps.core.interfaces import Service
from apps.notifications.senders.interface import Sender


class NotificationService(Service):
    def __init__(self, sender: Sender):
        self._sender = sender

    def execute(self, user_id: int, message: str) -> None:
        self._sender.send(user_id, message)
