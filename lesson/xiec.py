import asyncio
import time

now = lambda: time.time()


async def do_task_work(task):
    print('it is do task work', task)


start = now()
work = do_task_work(100)
loop = asyncio.get_event_loop()
loop.run_until_complete(work)
print('it work time', now() - start)
