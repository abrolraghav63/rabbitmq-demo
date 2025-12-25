import pika

# Connection parameters
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

print("Setting up RabbitMQ infrastructure...")

# Setup for Producer 1 / Consumer 1
channel.exchange_declare(exchange='user_contact_exchange', exchange_type='direct', durable=True)
channel.queue_declare(queue='user_contact_queue', durable=True)
channel.queue_bind(exchange='user_contact_exchange', queue='user_contact_queue', routing_key='user.contact')
print("✓ User contact exchange and queue created")

# Setup for Producer 2 / Consumer 2 / Consumer 3
channel.exchange_declare(exchange='user_billing_exchange', exchange_type='topic', durable=True)
channel.queue_declare(queue='user_billing_queue', durable=True)
channel.queue_bind(exchange='user_billing_exchange', queue='user_billing_queue', routing_key='user.billing')
print("✓ User billing queue created (all records)")

channel.queue_declare(queue='user_billing_india_queue', durable=True)
channel.queue_bind(exchange='user_billing_exchange', queue='user_billing_india_queue', routing_key='user.billing.india')
print("✓ User billing India queue created")

print("\nAll queues and exchanges are ready!")
print("Now you can run producers and consumers in any order.")

connection.close()
