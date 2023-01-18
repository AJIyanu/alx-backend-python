#!/usr/bin/env python3
"""multiple coroutines at the same time"""


import asyncio
from random import random
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """run dont wait"""
    task = []
    for i in range(n):
        task.append(await task_wait_random(max_delay))
    return sorted(await asyncio.gather(*task.result()))
