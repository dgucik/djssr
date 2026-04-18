from apps.notifications.senders.interface import Sender


class EmailSender(Sender):
    def send(self, user_id: int, message: str) -> None:
        print(f"Sending email to user {user_id}: {message}")