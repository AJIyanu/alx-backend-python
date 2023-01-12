#!/usr/bin/env python3
"""generator to yield random number"""


from time import sleep
from random import randrange


def async_generator():
    """generate random shits"""
    sleep(1)
    yield random() + randrange(1, 10)
