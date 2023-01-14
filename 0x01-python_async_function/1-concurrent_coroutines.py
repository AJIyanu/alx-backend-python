#!/usr/bin/env python3
"""multiple coroutines at the same time"""


import asyncio
from random import random
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random



async def wait_n(n: int, max_delay: int) -> List[float]:
    """run dont wait"""
    colst: List[float] = []
    #task = wait_random(max_delay)
    for i in range(n):
        try:
            task = asyncio.create_task(wait_random(max_delay))
            print(f"started task {i}")
            await task
            colst.append(task)
        except Exception:
            print(f"couldn't start task {i}")
        #colst.append(await task)
    #await task
    return colst
