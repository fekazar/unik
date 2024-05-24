import datetime

import pika, sys, os

EMAIL_QUEUE = 'email'
LOG_FILE = "messages.log"

log_file = open(LOG_FILE, 'a')

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=EMAIL_QUEUE)

    def callback(ch, method, properties, body):
        log_file.write('Received: ' + body.decode() + ' at: ' + str(datetime.datetime.now()) + '\n')
        log_file.flush()

    channel.basic_consume(queue=EMAIL_QUEUE, on_message_callback=callback, auto_ack=True)
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
