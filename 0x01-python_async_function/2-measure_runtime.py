#!/usr/bin/env python3
"""
Module 2-measure_runtime
"""

import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


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
    start_time = perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end_time = perf_counter()
    total_time = end_time - start_time
    return total_time / n
