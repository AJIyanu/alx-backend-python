#!/usr/bin/env python3
"""create and return async task"""


import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """return an asyncio task"""
    return asyncio.Task(wait_random(max_delay))
