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
exchange_name = 'user_billing_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)

print(f'Producer 2 connected. Publishing to exchange: {exchange_name}')

# Sample data - user, mobilenum, country, bill
data = [
    {'user': 'Alice', 'mobilenum': '9876543210', 'country': 'India', 'bill': 500},
    {'user': 'Bob', 'mobilenum': '9876543211', 'country': 'USA', 'bill': 800},
    {'user': 'Charlie', 'mobilenum': '9876543212', 'country': 'India', 'bill': 450},
    {'user': 'Diana', 'mobilenum': '9876543213', 'country': 'UK', 'bill': 700},
    {'user': 'Eve', 'mobilenum': '9876543214', 'country': 'India', 'bill': 550},
    {'user': 'Frank', 'mobilenum': '9876543215', 'country': 'Canada', 'bill': 650},
]

try:
    for i, record in enumerate(data):
        message = json.dumps(record)
        
        # Publish to user.billing routing key (all messages)
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='user.billing',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f"[Producer 2] Sent message {i+1} to user.billing: {record}")
        
        # If India, also publish to user.billing.india routing key
        if record['country'] == 'India':
            channel.basic_publish(
                exchange=exchange_name,
                routing_key='user.billing.india',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )
            print(f"[Producer 2] Also sent message {i+1} to user.billing.india")
        
        time.sleep(1)
    
    print("\n[Producer 2] All messages sent successfully!")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()
