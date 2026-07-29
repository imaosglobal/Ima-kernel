from abc import ABC, abstractmethod

class UniversalAdapter(ABC):
    """Universal contract for connecting IMA to external technologies."""

    @abstractmethod
    def discover(self): ...

    @abstractmethod
    def connect(self, config=None): ...

    @abstractmethod
    def capabilities(self): ...

    @abstractmethod
    def execute(self, action, payload=None): ...

    @abstractmethod
    def observe(self): ...

    @abstractmethod
    def verify(self, result): ...

    @abstractmethod
    def disconnect(self): ...
