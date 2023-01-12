#!/usr/bin/env python3
"""generator to yield random number"""


from time import sleep
from random import randrange


def async_generator():
    """generate random shits"""
    yield random() + randrange(0, 10)
    sleep(1)
