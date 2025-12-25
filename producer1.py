import pika
import json
import time

# Connection parameters
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

# Declare exchange
exchange_name = 'user_contact_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

# Declare queue
queue_name = 'user_contact_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Bind queue to exchange
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.contact')

print(f'Producer 1 connected. Publishing to exchange: {exchange_name}')

# Sample data - user and mobilenumber
data = [
    {'user': 'Alice', 'mobilenumber': '9876543210'},
    {'user': 'Bob', 'mobilenumber': '9876543211'},
    {'user': 'Charlie', 'mobilenumber': '9876543212'},
    {'user': 'Diana', 'mobilenumber': '9876543213'},
    {'user': 'Eve', 'mobilenumber': '9876543214'},
]

try:
    for i, record in enumerate(data):
        message = json.dumps(record)
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='user.contact',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f"[Producer 1] Sent message {i+1}: {record}")
        time.sleep(1)
    
    print("\n[Producer 1] All messages sent successfully!")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()
