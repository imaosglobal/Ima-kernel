import os
from abc import ABC, abstractmethod


class BillingAdapter(ABC):
    provider_id = None
    required_env = ()

    @classmethod
    def is_configured(cls):
        return all(os.getenv(key) for key in cls.required_env)

    @abstractmethod
    def create_checkout(self, customer, product):
        raise NotImplementedError

    @abstractmethod
    def verify_payment(self, payload):
        raise NotImplementedError

    @abstractmethod
    def handle_webhook(self, payload, signature=None):
        raise NotImplementedError
