#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Callable
from time import sleep
import random
import time

DEFAULT_CHANNEL = "test"
VERBOSE = 0
TIME_PR_PRODUCE = 0.02
TIME_PR_CONSUME = 0.2


def get_self_name(self):
    return str(hash(self))[-3:]


# +-1 20% tops
def _get_random_mod():
    return 1 - (random.random() * 2 - 1) * 0.5


class Clearer(ABC):
    @abstractmethod
    def clear_queue(self) -> None:
        pass


class Producer(ABC):
    @abstractmethod
    def send(self, msg: str) -> None:
        pass

    def start_test(self, msg_count=10):
        name = get_self_name(self)
        for i in range(msg_count):
            msg = f"{name}:{i}"
            if VERBOSE:
                print(f"[W] [{name}]: {msg}")
            self.send(f"{name}:{i}")
            sleep(TIME_PR_PRODUCE)


class Consumer(ABC):
    def callback(self, msg: str):
        name = get_self_name(self)
        if VERBOSE:
            print(f"[R] [{name}]: {msg.decode()}")
        sleep(TIME_PR_CONSUME)

    @abstractmethod
    def run(self):
        pass


class Logger(ABC):
    @abstractmethod
    def queue_length(self) -> int:
        pass

    def log(self):
        start_time = time.time()
        zero_time = None
        values_has_been_added = False
        while 1:
            run_time = time.time() - start_time
            length = self.queue_length()
            if length > 0:
                values_has_been_added = True
            if zero_time is None and values_has_been_added:
                if length == 0:
                    zero_time = time.time()
                else:
                    zero_time = None
            if zero_time is None:
                if VERBOSE:
                    print(f"Count = {self.queue_length()}")
                else:
                    print(
                        f"\r[STATUS: COUNT={length} TIME={run_time:.2f}s]", end="",
                    )
            sleep(0.2)
            if zero_time and zero_time + 3 < time.time():
                print("\nLength Has been zero for 3s - closing")
                return
