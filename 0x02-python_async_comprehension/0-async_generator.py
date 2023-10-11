#!/usr/bin/env python3
"""generator to yield random number"""

import asyncio
from typing import AsyncGenerator
from random import randrange, random


async def async_generator() -> AsyncGenerator[float, None]:
    """generate random shits"""
    for i in range(10):
        yield random() + randrange(0, 10)
        await asyncio.sleep(1)
