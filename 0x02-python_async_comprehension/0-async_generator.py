#!/usr/bin/env python3
"""generator to yield random number"""

import asyncio
from typing import Generator
from random import randrange, random


async def async_generator() -> Generator[float, None, None]:
    """generate random shits"""
    for i in range(10):
        yield random() + randrange(0, 10)
        await asyncio.sleep(1)
