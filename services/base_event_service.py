"Базовый класс сервисов"
from __future__ import annotations
from typing import List
from abc import ABCMeta, abstractmethod
from rx.core.abc.disposable import Disposable

from core import EventsEmitter


class BaseEventService(Disposable, metaclass=ABCMeta):
    "Базовый класс сервисов"

    def __init__(self, emitter: EventsEmitter):
        self.emitter = emitter
        self.subscriptions: List[Disposable] = list()

    @abstractmethod
    def init(self) -> None:
        "Инициализировать обработчики событий"

    def register_subscription(self, subscription: Disposable) -> None:
        "Зарегистрировать подписку"
        self.subscriptions.append(subscription)

    def register_subscriptions(self, subscriptions: List[Disposable]) -> None:
        "Зарегистрировать подписку"
        self.subscriptions.extend(subscriptions)

    def dispose(self) -> None:
        "Отписаться от всех событий"
        for subscription in self.subscriptions:
            subscription.dispose()
