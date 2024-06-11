#!/usr/bin/env python3
"""
Module 0-async_generator
"""

import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    """
    Coroutine that asynchronously generates 10 random numbers.

    This coroutine will loop 10 times, each time asynchronously waiting
    for 1 second, then yielding a random float number between 0 and 10.

    Yields:
        float: A random number between 0 and 10.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
