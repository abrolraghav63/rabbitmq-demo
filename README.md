# RabbitMQ Producer and Consumer Setup

## Requirements
```
pip install pika
```

## Running the Project

Make sure RabbitMQ is running on `localhost:5672` with default credentials (guest:guest).

### Important: Setup Infrastructure First

Before running producers and consumers, you must create the exchanges and queues:

```bash
python3 setup_infrastructure.py
```

This ensures all queues exist and are bound, so messages won't be lost even if consumers start late.

### Running Producers and Consumers

**You can now run producers and consumers in ANY order**

**Terminal 1 - Start Consumer 1 (listens to Producer 1):**
```bash
python3 consumer1.py
```

**Terminal 2 - Start Consumer 2 (listens to all Producer 2 messages):**
```bash
python3 consumer2.py
```

**Terminal 3 - Start Consumer 3 (listens to Producer 2, India only):**
```bash
python3 consumer3.py
```

**Terminal 4 - Run Producer 1:**
```bash
python3 producer1.py
```

**Terminal 5 - Run Producer 2:**
```bash
python3 producer2.py
```

## Project Overview

### Producers

**Producer 1** - Sends user contact data with `user` and `mobilenumber`
- Exchange: `user_contact_exchange` (direct exchange)
- Routing key: `user.contact`
- Queue: `user_contact_queue`

**Producer 2** - Sends user billing data with `user`, `mobilenum`, `country`, and `bill`
- Exchange: `user_billing_exchange` (topic exchange)
- Routing keys: 
  - `user.billing` - All billing records
  - `user.billing.india` - Only India billing records

### Consumers

**Consumer 1** - Reads all user contact records from Producer 1
- Queue: `user_contact_queue`
- Exchange: `user_contact_exchange`
- Routing key: `user.contact`

**Consumer 2** - Reads all billing records from Producer 2
- Queue: `user_billing_queue`
- Exchange: `user_billing_exchange`
- Routing key: `user.billing` (receives all billing messages)

**Consumer 3** - Reads only India billing records from Producer 2
- Queue: `user_billing_india_queue`
- Exchange: `user_billing_exchange`
- Routing key: `user.billing.india` (receives only India messages via RabbitMQ routing)

## Important Notes

### Message Delivery Guarantee

- **If queue doesn't exist when message is published** → Message is lost (no destination)
- **If queue exists but consumer is disconnected** → Message stays in queue until consumer reconnects ✅
- Always run `setup_infrastructure.py` first to pre-create all queues

### Consumer Disconnection

If a consumer disconnects temporarily:
1. The queue persists
2. Messages accumulate in the queue
3. When consumer reconnects, it receives all accumulated messages

This is the intended behavior for reliable message delivery.
# rabbitmq-demo
