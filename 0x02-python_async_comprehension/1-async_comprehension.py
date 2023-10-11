#!/usr/bin/env python3
"""creating async comprehension from generator"""


async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> list:
    """collects list from generator and creates a new"""
    return [i async for i in async_generator()]
