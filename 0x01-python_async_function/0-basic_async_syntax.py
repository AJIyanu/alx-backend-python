#!/usr/bin/env python3
"""azynchronois co routine"""


import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """wait randomly"""
    slep: float = random.uniform(0, max_delay)
    await asyncio.sleep(slep)
    return slep
