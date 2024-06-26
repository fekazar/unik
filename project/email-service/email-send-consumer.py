import pika, sys, os
import emailassist

RABBIT_HOST = os.getenv('RABBIT_HOST')
print(RABBIT_HOST)

EMAIL_LOGIN = os.getenv('MAIL_LOGIN')
EMAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

EMAIL_QUEUE = 'email'
ERROR_QUEUE = 'errorsqueue'
ERROR_EXCHANGE = 'errorexchange'

clients = []
with open('clients.txt') as clients_file:
    for line in clients_file:
        clients.append(line.strip())

email_sender = emailassist.EmailSender(EMAIL_LOGIN, EMAIL_PASSWORD)

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
#connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials))
#connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@broker:5672"))

channel = rabbit_connection.channel()

channel.queue_declare(queue=EMAIL_QUEUE)
channel.queue_declare(queue=ERROR_QUEUE)

channel.exchange_declare(exchange=ERROR_EXCHANGE,
                         exchange_type='direct')

channel.queue_bind(exchange=ERROR_EXCHANGE,
                   queue=ERROR_QUEUE)

print("Will send emails to these clients:", clients)

def main():
    def callback(ch, method, properties, body):
        try:
            for email in clients:
                email_sender.send_email(email, body.decode())
        except Exception as e:
            print("error: " + str(e))
            channel.basic_publish(ERROR_EXCHANGE,
                                  routing_key=ERROR_QUEUE,
                                  body=str(e))

    channel.basic_consume(queue=EMAIL_QUEUE, on_message_callback=callback, auto_ack=True)
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
