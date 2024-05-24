import pika

EXCHANGE = 'messagesexchange'

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    email_res = channel.queue_declare(queue='email')
    logs_res = channel.queue_declare(queue='logs')

    channel.exchange_declare(exchange=EXCHANGE,
                             exchange_type='fanout')

    channel.queue_bind(exchange=EXCHANGE,
                       queue=email_res.method.queue)

    channel.queue_bind(exchange=EXCHANGE,
                       queue=logs_res.method.queue)

    channel.basic_publish(exchange=EXCHANGE,
                          routing_key='',
                          body='fuck off')

    connection.close()

if __name__ == '__main__':
    main()

