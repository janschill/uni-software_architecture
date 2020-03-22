#!/usr/bin/env python3
"""
Based on
https://www.rabbitmq.com/tutorials/tutorial-one-python.html
and
https://www.rabbitmq.com/tutorials/tutorial-three-python.html
"""


from base import Producer, Consumer, Logger, Clearer, DEFAULT_CHANNEL
from typing import Callable, Dict, Any
import pika
import sys


class RabbitMQNode:
    def __init__(
        self,
        host: str,
        queue: str = DEFAULT_CHANNEL,
        queue_kwargs: Dict[str, Any] = {},
    ):
        self.host = host

        self.queue_name = queue
        self.connection = pika.BlockingConnection(pika.URLParameters(host))
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=queue, **queue_kwargs)


class RabbitMQClearer(RabbitMQNode, Clearer):
    def clear_queue(self) -> None:
        self.channel.queue_delete(queue=self.queue_name)


class RabbitMQProducer(Producer, RabbitMQNode):
    """
    RabbitMQProducer produces test messages and sends it to RabbitMQ via the `start` function.
    """

    def send(self, msg: str) -> None:
        self.channel.basic_publish(exchange="", routing_key=self.queue_name, body=msg)


class RabbitMQConsumer(Consumer, RabbitMQNode):
    """
    RabbitMQProducer consumes test messages and sends it to RabbitMQ via the `start` function.
    It will then simulate having to do an amount of work before popping a new message
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer_tag = None

    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        for method, _, body in self.channel.consume(
            self.queue_name, inactivity_timeout=1, auto_ack=False
        ):
            self.callback(body)
            if method:
                self.channel.basic_ack(delivery_tag=method.delivery_tag)
            else:
                break

        self.channel.close()
        self.connection.close()


class RabbitMQLogger(RabbitMQNode, Logger):
    """
    RabbitMQProducer produces test messages and sends it to RabbitMQ via the `start` function.
    """

    def queue_length(self) -> int:
        # this is the worst live I've ever written. But it is useful as we apparently
        # need to redefine the connection for rabbitMQ to give us the newest count
        super().__init__(self.host)
        return self.queue.method.message_count


KLASS_TUPLE = (RabbitMQProducer, RabbitMQConsumer, RabbitMQLogger, RabbitMQClearer)
