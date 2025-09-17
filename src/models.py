from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, client_handel, args):
        pass


class Subscriber(ABC):
    @abstractmethod
    def notify(self, topic, message):
        pass


class TopicManagerInterface(ABC):
    @abstractmethod
    def add_subscriber(self, topic, subscriber: Subscriber):
        pass

    @abstractmethod
    def remove_subscriber(self, topic, subscriber: Subscriber):
        pass

    @abstractmethod
    def publish(self, topic, message):
        pass
