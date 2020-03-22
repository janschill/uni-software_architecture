#!/usr/bin/env python3
from base import Producer, Consumer, Logger, DEFAULT_CHANNEL
import pulsar
# ONLY works in 3.6

class PulsarNode:
    def __init__(
        self, host: str, queue: str = DEFAULT_CHANNEL,
    ):
        self.client = pulsar.Client(host)
        self.consumer = self.client.subscribe(queue, subscription_name=queue)


class PulsarClearer(PulsarNode):
    def __init__(
        self, host: str, queue: str = DEFAULT_CHANNEL,
    ):
        self.client = pulsar.Client(host)
        self.producer = self.client.create_producer(queue)

    def clear_queue(self, queue: str = DEFAULT_CHANNEL) -> None:
        self.consumer.queue_delete(queue=queue)


class PulsarProducer(Producer):
    """
    RabbitMQProducer produces test messages and sends it to RabbitMQ via the `start` function.
    """

    def __init__(
        self, host: str, queue: str = DEFAULT_CHANNEL,
    ):
        self.client = pulsar.Client(host)
        self.producer = self.client.create_producer(queue)

    def send(self, msg: str) -> None:
        self.producer.send_async(msg.encode("utf-8"))


class PulsarConsumer(Consumer):
    """
    RabbitMQProducer consumes test messages and sends it to RabbitMQ via the `start` function.
    It will then simulate having to do an amount of work before popping a new message
    """

    def __init__(
        self, host: str, queue: str = DEFAULT_CHANNEL,
    ):
        self.client = pulsar.Client(host)
        self.consumer = self.client.create_reader(queue, subscription_name=queue)

    def run(self):
        while True:
            msg = self.consumer.receive()
            self.callback(msg)
            self.consumer.acknowledge(msg)


class PulsarLogger(Logger):
    """
    RabbitMQProducer produces test messages and sends it to RabbitMQ via the `start` function.
    """

    def queue_length(self) -> int:
        return -1


KLASS_TUPLE = (PulsarProducer, PulsarConsumer, PulsarLogger, PulsarClearer)
