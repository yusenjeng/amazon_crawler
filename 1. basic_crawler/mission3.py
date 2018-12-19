import asyncio
import time
import random


def add_simple(x, y):
    print("Add %s + %s ..." % (x, y))
    time.sleep(random.randrange(1, 10))
    print(x+y)


print('Before')
add_simple(1, 1)
add_simple(2, 2)
add_simple(3, 3)
print('After')


print('========================')


async def add(x, y):
    print("Add %s + %s ..." % (x, y))
    await asyncio.sleep(random.randrange(1, 10))
    print(x+y)


print('Before')
tasks = []
tasks.append(add(1, 1))
tasks.append(add(2, 2))
tasks.append(add(3, 3))
print('After')


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()
