#!/usr/bin/env python3
"""azynchronois co routine"""


import asyncio
import random


async def wait_random(max_delay: int = 10) -> int:
    """wait randomly"""
    slep = random.randrange(0, max_delay) + random.random()
    await asyncio.sleep(slep)
    return slep
