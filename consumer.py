import json
import os
import time


import pika

from main import Product, db

RABBIT_ENDPOINT = os.environ['RABBIT_ENDPOINT']


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')


class Consumer:
    """Implement the consumer script."""

    def start(self, connection):
        # if not self.connection or self.connection.is_closed:
        #     self.connection = pika.BlockingConnection(self.params)
        channel = connection.channel()
        channel.queue_declare(queue='main')
        channel.basic_consume(
            queue='main',
            on_message_callback=callback,
            auto_ack=True,
        )
        print('Started Consuming in queue: main...')
        channel.start_consuming()
        channel.close()


print('Starting the connection to message queue.....')
consumer = Consumer()
params = pika.URLParameters(RABBIT_ENDPOINT)
while True:
    try:
        connection = pika.BlockingConnection(params)
    except:
        print('could not connect to the host: {0}. retrying in 1 sec...'.format(RABBIT_ENDPOINT))
        time.sleep(1)
        continue
    consumer.start(connection)
