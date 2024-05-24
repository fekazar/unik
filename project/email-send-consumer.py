import pika, sys, os

EMAIL_QUEUE = 'email'
ERROR_QUEUE = 'errorsqueue'
ERROR_EXCHANGE = 'errorexchange'

clients = []
with open('clients.txt') as clients_file:
    for line in clients_file:
        clients.append(line.strip())

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

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
            # todo: send email to clients from client list
            raise RuntimeError("Test error")
        except Exception as e:
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
            connection.close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
