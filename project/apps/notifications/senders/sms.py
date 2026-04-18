from apps.notifications.senders.interface import Sender


class SmsSender(Sender):
    def send(self, user_id: int, message: str) -> None:
        print(f"Sending SMS to user {user_id}: {message}")