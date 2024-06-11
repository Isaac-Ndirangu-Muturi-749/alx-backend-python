#!/usr/bin/env python3
"""
Module 2-measure_runtime
"""

import asyncio
from typing import List
import time
from concurrent_coroutines import wait_n


async def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the total execution time for wait_n(n, max_delay) and
    returns total_time / n.

    Args:
        n (int): The number of times to call wait_n.
        max_delay (int): The maximum delay for wait_n.

    Returns:
        float: The average execution time per call.
    """
    start_time = time.time()

    await wait_n(n, max_delay)

    end_time = time.time()

    total_time = end_time - start_time
    return total_time / n
