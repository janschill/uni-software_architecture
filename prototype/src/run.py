#!/usr/bin/env python3
from typing import Any, Callable
import threading

from rabbitmq import KLASS_TUPLE as RABBIT_KLASS_TUPLE

from base import Producer, Consumer

PROVIDERS = {"RabbitMQ": RABBIT_KLASS_TUPLE}
SHORT_NAMES = {key[0].lower(): key for key in PROVIDERS}
HOST = "localhost"


def query_input(label: str, callback: Callable[[str], Any]) -> Any:
    count = 0
    while True:
        answer = input(label)
        # Python believes in `ask for forgiveness rather than permission`
        try:
            # Python doesn't have shitty scoping rules,
            # so i don't have to define this in the outer scope
            return callback(answer)
        except (KeyError, ValueError):
            if count < 2:
                print("Invalid answer.")
            else:
                print("ARE YOU STUPID?")
            count += 1


def run_test():
    print("Which provider do you want to test?\nPlease pick one of:")
    # This is just pythonic magic to create what is essentially a map function
    print("\n".join(f"[{k}]: {name}" for k, name in SHORT_NAMES.items()))

    producer_klass, consumer_klass, logger_klass, clearer_klass = query_input(
        "answer: ", lambda ans: PROVIDERS[SHORT_NAMES[ans.lower()]]
    )
    producer_count = query_input("producer count: ", lambda ans: int(ans))
    producer_msg_count = query_input("messages pr producer: ", lambda ans: int(ans))
    consumer_count = query_input("consumer count: ", lambda ans: int(ans))

    # clearer_klass(HOST).clear_queue()

    producer_threads = [
        threading.Thread(
            target=producer_klass(HOST).start_test,
            kwargs={"msg_count": producer_msg_count},
        )
        for _ in range(producer_count)
    ]
    consumers = [consumer_klass(HOST) for _ in range(consumer_count)]
    consumer_threads = [threading.Thread(target=consumer.run) for consumer in consumers]
    logger = logger_klass(HOST)
    print("starting consumers..")
    for t in consumer_threads:
        t.start()
    print("finished")
    print("starting producers..")
    for t in producer_threads:
        t.start()

    print("finished")
    print("Running..")
    log_thread = threading.Thread(target=logger.log)
    log_thread.start()

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
