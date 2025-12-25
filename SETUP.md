# RabbitMQ Setup on Ubuntu Jammy (22.04)

## Prerequisites
- Ubuntu 22.04 (Jammy) VM
- sudo access
- Internet connection

## Installation Steps

### 1. Update System Packages
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Install Erlang (Required by RabbitMQ)
```bash
sudo apt-get install erlang-base -y
```

### 3. Add RabbitMQ Repository
```bash
curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/v2/rabbitmq-release-signing-key.asc | sudo apt-key add -
```

Add the official RabbitMQ repository:
```bash
sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
deb https://dl.bintray.com/rabbitmq-erlang/debian jammy erlang
deb https://dl.bintray.com/rabbitmq/debian jammy main
EOF
```

### 4. Update Repository Cache
```bash
sudo apt-get update
```

### 5. Install RabbitMQ Server
```bash
sudo apt-get install rabbitmq-server -y
```

### 6. Start RabbitMQ Service
```bash
sudo systemctl start rabbitmq-server
```

### 7. Enable RabbitMQ on Boot
```bash
sudo systemctl enable rabbitmq-server
```

### 8. Verify RabbitMQ is Running
```bash
sudo systemctl status rabbitmq-server
```

### 9. Enable Management Plugin (Optional but Recommended)
The management plugin provides a web UI to monitor and manage RabbitMQ:
```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

Restart RabbitMQ to apply changes:
```bash
sudo systemctl restart rabbitmq-server
```

## Post-Installation Configuration

### 1. Create Default User (if needed)
RabbitMQ comes with default guest user (username: `guest`, password: `guest`).

To add a new user:
```bash
sudo rabbitmqctl add_user <username> <password>
sudo rabbitmqctl set_permissions -p / <username> ".*" ".*" ".*"
sudo rabbitmqctl set_user_tags <username> administrator
```

### 2. Access RabbitMQ Management UI
- URL: `http://localhost:15672` or `http://<VM-IP>:15672`
- Default credentials: `guest:guest`

### 3. Test RabbitMQ Connection
```bash
# Check if RabbitMQ is listening on port 5672
sudo netstat -tulpn | grep 5672

# Or using ss command
sudo ss -tulpn | grep 5672
```

## Firewall Configuration (if needed)

If you have a firewall enabled, allow RabbitMQ ports:
```bash
# AMQP port (client connections)
sudo ufw allow 5672/tcp

# Management UI port
sudo ufw allow 15672/tcp
```

## Useful Commands

### Check RabbitMQ Status
```bash
sudo systemctl status rabbitmq-server
```

### Start/Stop RabbitMQ
```bash
sudo systemctl start rabbitmq-server
sudo systemctl stop rabbitmq-server
sudo systemctl restart rabbitmq-server
```

### View RabbitMQ Logs
```bash
sudo tail -f /var/log/rabbitmq/rabbit@<hostname>.log
```

### Reset RabbitMQ (Reset to Factory Settings)
```bash
sudo rabbitmqctl reset
sudo systemctl restart rabbitmq-server
```

### List Users
```bash
sudo rabbitmqctl list_users
```

### Delete a User
```bash
sudo rabbitmqctl delete_user <username>
```

## Python Dependencies Installation

### 1. Install Python and pip (if not already installed)
```bash
sudo apt-get install python3 python3-pip -y
```

### 2. Install Required Python Packages
Navigate to the project directory and install dependencies:
```bash
cd /path/to/RabbitMQ
pip install -r requirements.txt
```

Or install pika directly:
```bash
pip3 install pika==1.3.2
```

### 3. Verify pika Installation
```bash
python3 -c "import pika; print(pika.__version__)"
```

## Default Connection Details for Python

When running the Python producer/consumer scripts:
- **Host**: `localhost` (or your VM IP address)
- **Port**: `5672`
- **Username**: `guest`
- **Password**: `guest`
- **Virtual Host**: `/` (default)

## Troubleshooting

### RabbitMQ won't start
```bash
# Check if Erlang is installed
erl -version

# Check system resources
free -h
df -h

# Check RabbitMQ logs
sudo journalctl -u rabbitmq-server -n 100
```

### Connection Refused Error
- Verify RabbitMQ is running: `sudo systemctl status rabbitmq-server`
- Check if firewall is blocking port 5672
- Ensure you're using the correct IP address (not localhost if connecting from another machine)

### Management UI not accessible
- Verify the management plugin is enabled: `sudo rabbitmq-plugins list | grep management`
- Re-enable if needed: `sudo rabbitmq-plugins enable rabbitmq_management`
- Wait 10-15 seconds after restarting RabbitMQ

## Next Steps

Once RabbitMQ is running and Python dependencies are installed:
1. Run the producer and consumer scripts from this repository
2. Monitor messages in the Management UI dashboard
