import pika
import json

# Connection parameters
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

# Declare exchange and queue (same as Producer 2)
exchange_name = 'user_billing_exchange'
queue_name = 'user_billing_queue'

channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
channel.queue_declare(queue=queue_name, durable=True)
# Bind to user.billing routing key (all messages)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.billing')

print(f'Consumer 2 connected. Listening to queue: {queue_name}')
print('Waiting for messages from Producer 2...\n')

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"[Consumer 2] Received: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up consumer
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n[Consumer 2] Stopped consuming")
    connection.close()
