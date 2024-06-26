import datetime
import pika, sys, os

RABBIT_HOST = os.getenv('RABBIT_HOST')

ERROR_QUEUE = 'errorsqueue'
ERROR_EXCHANGE = 'errorexchange'
LOGS_QUEUE = 'logs'
LOG_FILE = "logs/messages.log"

log_file = open(LOG_FILE, 'a')

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


channel = rabbit_connection.channel()
channel.queue_declare(queue=LOGS_QUEUE)
channel.queue_declare(queue=ERROR_QUEUE)

channel.exchange_declare(exchange=ERROR_EXCHANGE,
                         exchange_type='direct')

channel.queue_bind(exchange=ERROR_EXCHANGE,
                   queue=ERROR_QUEUE)

def main():
    def callback(ch, method, properties, body):
        try:
            log_file.write('Received: ' + body.decode() + ' at: ' + str(datetime.datetime.now()) + '\n')
            log_file.flush()
        except Exception as e:
            channel.basic_publish(ERROR_EXCHANGE,
                                  routing_key=ERROR_QUEUE,
                                  body=str(e))

    channel.basic_consume(queue=LOGS_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            rabbit_connection.close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
