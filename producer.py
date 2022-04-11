import json
import os

import pika

RABBIT_ENDPOINT = os.environ['RABBIT_ENDPOINT']


class Producer:
    """Implement the producer logic."""

    def __init__(self):
        self.params = pika.URLParameters(RABBIT_ENDPOINT)
        self.connection = pika.BlockingConnection(self.params)

    def publish(self, method, body):
        properties = pika.BasicProperties(method)
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.params)
        channel = self.connection.channel()
        channel.basic_publish(
            exchange='',
            routing_key='admin',
            body=json.dumps(body),
            properties=properties,
        )
        print('Product published in queue: MAIN')
