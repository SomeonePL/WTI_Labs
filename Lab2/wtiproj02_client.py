import redis
from time import sleep
from json import loads

red = redis.Redis(
    host='localhost',
    port=6381
)

while True:
    sleep(0.01)
    fakejson = red.lpop('queue')
    print(loads(fakejson))

