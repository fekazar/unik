import requests
import json
import redis, pika
import sys, os, time

RABBIT_HOST = os.getenv('RABBIT_HOST')
REDIS_HOST = os.getenv('REDIS_HOST')

PARSE_INTERVAL = 15
KEY = "goodkey"
EXCHANGE = 'messagesexchange'

# Configuration
redis_client = redis.Redis(REDIS_HOST)
credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBIT_HOST,
                port=5672,
                credentials=credentials,
                heartbeat=0,
                blocked_connection_timeout=300,
            )
        )

rabbit_channel = rabbit_connection.channel()

email_res = rabbit_channel.queue_declare(queue='email')
logs_res = rabbit_channel.queue_declare(queue='logs')

rabbit_channel.exchange_declare(exchange=EXCHANGE,
                         exchange_type='fanout')

rabbit_channel.queue_bind(exchange=EXCHANGE,
                   queue=email_res.method.queue)

rabbit_channel.queue_bind(exchange=EXCHANGE,
                   queue=logs_res.method.queue)

def job():
    time_response = requests.get("https://worldtimeapi.org/api/timezone/Europe/Moscow",
                                 headers={"Content-Type": "application/json"})
    data = json.loads(time_response.text)
    res_time = data["utc_datetime"]

    prev_time = redis_client.get(KEY)
    if prev_time != res_time:
        redis_client.set(KEY, res_time)
        print(res_time)

        rabbit_channel.basic_publish(exchange=EXCHANGE,
                                     routing_key='',
                                     body=json.dumps({ "text" : res_time }))

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
            rabbit_connection.close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)

