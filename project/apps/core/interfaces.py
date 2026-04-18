from abc import ABC, abstractmethod
from typing import Any
    

class Service(ABC):
    def __call__(self, *args, **kwargs) -> Any:
        return self.execute(*args, **kwargs)

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass