#!/usr/bin/env python3
from typing import Any, Callable
import threading

from rabbitmq_controller import KLASS_TUPLE as RABBIT_KLASS_TUPLE
from pulsar_controller import KLASS_TUPLE as PULSAR_KLASS_TUPLE
from kafka_controller import KLASS_TUPLE as KAFKA_KLASS_TUPLE

from base import Producer, Consumer

# Initialize a dictionary
PROVIDERS = {
    "RabbitMQ": (*RABBIT_KLASS_TUPLE, "amqp://localhost"),
    "CloudAMQP": (
        *RABBIT_KLASS_TUPLE,
        "amqp://cyumjzzf:Mr0602WRPkQi20MzbqGLhSUzyA_B1yuo@hawk.rmq.cloudamqp.com/cyumjzzf",
    ),
    "Pulsar": (*PULSAR_KLASS_TUPLE, "localhost"),
    "Kafka": (*KAFKA_KLASS_TUPLE, "localhost:9092"),
}
#Pythons way of providing a map function on dictionaries.
# output is a dict like {"r":"RabbitMQ", "c":"CloudAMQP"...}
SHORT_NAMES = {key[0].lower(): key for key in PROVIDERS}
HOST = "localhost"


def query_input(label: str, callback: Callable[[str], Any]) -> Any:
    """
    Helper function for making the user provide input
    """
    count = 0
    while True:
        answer = input(label)
        # Python believes in `ask for forgiveness rather than permission`
        try:
            return callback(answer)
        except (KeyError, ValueError):
            if count < 1:
                print("Invalid answer.")
            else:
                print("ARE YOU STUPID?")
            count += 1


def run_test():
    print("Which provider do you want to test?\nPlease pick one of:")
    # This is just pythonic magic to create what is essentially a map function
    print("\n".join(f"[{k}]: {name}" for k, name in SHORT_NAMES.items()))

    # unpacks the returned tuple
    producer_klass, consumer_klass, logger_klass, clearer_klass, host = query_input(
        "answer: ", lambda ans: PROVIDERS[SHORT_NAMES[ans.lower()]]
    )
    producer_count = query_input("producer count: ", lambda ans: int(ans))
    producer_msg_count = query_input("messages pr producer: ", lambda ans: int(ans))
    consumer_count = query_input("consumer count: ", lambda ans: int(ans))

    # initializes the different classes and does shit

    clearer_klass(host).clear_queue()
    logger = logger_klass(host)
    log_thread = threading.Thread(target=logger.log)
    log_thread.start()
    print("\ncreating producers")
    producer_threads = [
        threading.Thread(
            target=producer_klass(host).start_test,
            kwargs={"msg_count": producer_msg_count},
        )
        for _ in range(producer_count)
    ]
    print("\ncreated - creating consumers")
    # mapping over the list of numbers between 0 and consumer_count and creates instances based on the class
    consumers = [consumer_klass(host) for _ in range(consumer_count)]
    # Mapping the list of consumers and creates threads from each and returns those
    consumer_threads = [threading.Thread(target=consumer.run) for consumer in consumers]
    print("\ncreated - starting consumers..")
    for t in consumer_threads:
        t.start()
    print("\nstarted - starting producers..")
    for t in producer_threads:
        t.start()

    print("\nstarted - running..")

    for t in producer_threads:
        t.join()
    print("\nFinished producing")
    log_thread.join()

    for t in consumer_threads:
        t.join()


# this checks if the interpreter is run from this file
# and therefore only runs the below code if that is the case
# contrary to forinstance this file being imported
# it's sorta like defining a Main in java ISH (VERY ISH)
if __name__ == "__main__":
    run_test()
