#!/usr/bin/env python3
"""
Module 3-tasks
"""

import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Creates an asyncio.Task for wait_random with the specified max_delay.

    Args:
        max_delay (int): The maximum delay for wait_random.

    Returns:
        asyncio.Task: The created asyncio.Task.
    """
    return asyncio.create_task(wait_random(max_delay))
