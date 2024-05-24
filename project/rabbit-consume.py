import pika, sys, os
import json

EMAIL_QUEUE = 'email'

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=EMAIL_QUEUE)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(data)

    channel.basic_consume(queue=EMAIL_QUEUE, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
