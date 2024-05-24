import requests
import json
import redis
import sys, os, time

PARSE_INTERVAL = 10
KEY = "goodkey"

redis_client = redis.Redis()

def job():
    time_response = requests.get("https://worldtimeapi.org/api/timezone/Europe/Moscow",
                                 headers={"Content-Type": "application/json"})
    data = json.loads(time_response.text)
    res_time = data["utc_datetime"]

    prev_time = redis_client.get(KEY)
    if prev_time != res_time:
        redis_client.set(KEY, res_time)
        print(res_time)

def main():
    while (True):
        job()
        time.sleep(PARSE_INTERVAL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            redis_client.close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)

