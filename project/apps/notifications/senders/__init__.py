from apps.notifications.senders.interface import Sender

__all__ = ['Sender', 'get_sender']

def get_sender(sender_type: str) -> Sender:
    if sender_type == 'sms':
        from apps.notifications.senders.sms import SmsSender
        return SmsSender()
    elif sender_type == 'email':
        from apps.notifications.senders.email import EmailSender
        return EmailSender()
    else:
        raise ValueError(f"Unsupported sender type: {sender_type}")