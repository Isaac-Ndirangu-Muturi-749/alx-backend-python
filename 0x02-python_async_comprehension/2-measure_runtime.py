#!/usr/bin/env python3
"""
Module 2-measure_runtime
"""

import asyncio
import time
from typing import List

async_comprehension = __import__("1_async_comprehensio").async_comprehension


async def measure_runtime() -> float:
    """
    Coroutine that measures the total runtime of executing async_comprehension
      four times in parallel.

    This coroutine uses asyncio.gather to run four instances of
      async_comprehension concurrently.
    It measures and returns the total runtime of this execution.

    Returns:
        float: The total runtime in seconds.
    """
    start_time = time.time()

    # Run async_comprehension four times in parallel
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
    )
    
    end_time = time.time()
    return end_time - start_time
