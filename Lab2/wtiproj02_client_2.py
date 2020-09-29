import redis
from time import sleep
from json import loads

red = redis.Redis(
    host='localhost',
    port=6381
)

n = 0
while n < 40:
    sleep(1)
    fakejson = red.lpop('queue')
    print(fakejson)
    if fakejson:
        print(loads(fakejson))
    n += 1

