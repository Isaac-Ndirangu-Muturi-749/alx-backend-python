#!/usr/bin/env python3

import asyncio

measure_runtime = __import__('2-measure_runtime').measure_runtime


async def main():
    """
    Main coroutine to execute measure_runtime and print the result.

    This coroutine will await the execution of measure_runtime and
    print the total runtime of running async_comprehension four times in parallel.
    """
    runtime = await measure_runtime()
    print(runtime)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
