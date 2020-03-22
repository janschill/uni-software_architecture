#!/usr/bin/env python3


from base import Producer, Consumer, Logger, Clearer, DEFAULT_CHANNEL
from typing import Callable, Dict, Any
from kafka import KafkaConsumer as KafkaExternalConsumer
from kafka import KafkaProducer as KafkaExternalProducer
from kafka import TopicPartition


class KafkaClearer(Clearer):
    def clear_queue(self) -> None:
        pass


class KafkaProducer(Producer):
    def __init__(self, host: str, topic: str = DEFAULT_CHANNEL) -> None:
        self.producer = KafkaExternalProducer(bootstrap_servers=host)
        self.topic = topic

    def send(self, msg: str) -> None:
        self.producer.send(self.topic, msg.encode())


class KafkaConsumer(Consumer):
    def __init__(self, host: str, topic: str = DEFAULT_CHANNEL) -> None:
        self.consumer = KafkaExternalConsumer(
            bootstrap_servers=host,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        self.consumer.assign([TopicPartition(topic, 2)])

    def run(self):
        for msg in self.consumer:
            print(msg.value)
            self.callback(msg.value)


class KafkaLogger(Logger):
    def __init__(self, host: str, topic: str = DEFAULT_CHANNEL) -> None:
        self.consumer = KafkaExternalConsumer(
            bootstrap_servers=host, consumer_timeout_ms=3000
        )
        self.consumer.assign([TopicPartition(topic, 2)])

    def queue_length(self) -> int:
        return self.consumer.metrics()["kafka-metrics-count"]["count"]


KLASS_TUPLE = (KafkaProducer, KafkaConsumer, KafkaLogger, KafkaClearer)
