import threading

from models import TopicManagerInterface


class TopicManager(TopicManagerInterface):
    def __init__(self):
        self.topics = {}
        self.lock = threading.Lock()

    def add_subscriber(self, topic, subscriber):
        with self.lock:
            subs = self.topics.setdefault(topic, [])
            if subscriber not in subs:
                subs.append(subscriber)

    def remove_subscriber(self, topic, subscriber):
        with self.lock:
            if topic in self.topics and subscriber in self.topics[topic]:
                self.topics[topic].remove(subscriber)

    def publish(self, topic, message):
        with self.lock:
            for sub in list(self.topics.get(topic, [])):
                try:
                    sub.notify(topic, message)
                except:  # noqa
                    self.topics[topic].remove(sub)
