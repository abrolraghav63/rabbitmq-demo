# RabbitMQ Producer and Consumer Setup

## Requirements
```
pip install pika
```

## Running the Project

Make sure RabbitMQ is running on `localhost:5672` with default credentials (guest:guest).

### Running Producers and Consumers

**Terminal 1 - Start Consumer 1 (listens to Producer 1):**
```bash
python consumer1.py
```

**Terminal 2 - Start Consumer 2 (listens to all Producer 2 messages):**
```bash
python consumer2.py
```

**Terminal 3 - Start Consumer 3 (listens to Producer 2, India only):**
```bash
python consumer3.py
```

**Terminal 4 - Run Producer 1:**
```bash
python producer1.py
```

**Terminal 5 - Run Producer 2:**
```bash
python producer2.py
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

## Features

- ✅ Message persistence (durable queues and messages)
- ✅ Direct exchange for Producer 1 (user contact data)
- ✅ Topic exchange for Producer 2 (user billing data with country-based routing)
- ✅ Acknowledgment of processed messages
- ✅ JSON message format
- ✅ Broker-level filtering for India records (no client-side filtering)
- ✅ Easy to extend with more producers/consumers
# rabbitmq-demo
