#!/usr/bin/env python3
"""run comprehension four time and return time"""


import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """return time taken to run comprehension"""
    start: float = time.time()
    await asyncio.gather(async_comprehension(), async_comprehension(),
                         async_comprehension(), async_comprehension())
    end: float = time.time()
    return end - start
