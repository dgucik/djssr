from abc import ABC, abstractmethod


class Sender(ABC):
    @abstractmethod
    def send(self, user_id: int, message: str) -> None:
        pass