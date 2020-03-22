#!/usr/bin/env python3
from base import Producer, Consumer, Logger, DEFAULT_CHANNEL
from pulsar import ConsumerType
import pulsar
# ONLY works in 3.6

done = False

class PulsarNode:
    def __init__(self, host: str, queue: str = DEFAULT_CHANNEL):
        pass

class PulsarClearer(PulsarNode):
    def __init__(self, host: str, queue: str = DEFAULT_CHANNEL):
        pass

    def clear_queue(self, queue: str = DEFAULT_CHANNEL) -> None:
        pass

class PulsarProducer(Producer):
    def __init__(self, host: str, queue: str = DEFAULT_CHANNEL):
        self.client = pulsar.Client("pulsar://127.0.0.1:6650")
        self.producer = self.client.create_producer('my-topic', batching_enabled=False)

    def send(self, msg: str) -> None:
        self.producer.send(msg.encode("utf-8"))

class PulsarConsumer(Consumer):
    def __init__(self, host: str, queue: str = DEFAULT_CHANNEL):
        self.client = pulsar.Client("pulsar://127.0.0.1:6650")
        self.consumer = self.client.subscribe('my-topic', 'my-subscription', consumer_type=ConsumerType.Shared)

    def run(self):
        global done

        while True:
            try:
                msg = self.consumer.receive(timeout_millis=1000)
                
                try:
                    self.callback(msg.data())
                    self.consumer.acknowledge(msg)
                except:
                    self.consumer.negative_acknowledge(msg)
            except:
                break

        self.consumer.close()
        self.client.close()
        done = True

class PulsarLogger(PulsarNode, Logger):
    def queue_length(self) -> int:
        global done, count

        if done == True:
            return 0
        else:
            return 1


KLASS_TUPLE = (PulsarProducer, PulsarConsumer, PulsarLogger, PulsarClearer)
