#!/usr/bin/env python3
"""multiple coroutines at the same time"""


import asyncio
from random import random
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random



async def wait_n(n: int, max_delay: int) -> List[float]:
    """run dont wait"""
    colst: List[float] = []
    task = asyncio.create_task(wait_random(max_delay))
    await task
    return task[result]
