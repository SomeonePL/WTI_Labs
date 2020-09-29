import redis
from time import sleep
from json import dumps
from faker import Faker
import pandas as pd

df = pd.read_csv('../user_ratedmovies.dat.txt', nrows=100, sep='\t', dtype={"userID": int})
df = df.astype(object)
red = redis.Redis(
    host='localhost',
    port=6381
)

remains = red.lrange('queue', 0, -1)
red.ltrim('queue', len(remains), -1)
fake = Faker('en_US')
while True:
    for index, row in df.iterrows():
        red.rpush('queue', row.to_json(orient='columns'))
        sleep(1)

    # fakejson = {'name': fake.name(), 'details' :{ 'age': randint(1, 99), 'shoe_nmbr': randint(1, 10)}}
    # print(fakejson)
    # sleep(0.01)
    # red.rpush('queue', dumps(fakejson))
    # print("Sent")
    #
