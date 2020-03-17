# Message Queue prototype

## Getting started

1. Make sure `docker-compose` and `Docker` are installed
2. Run `docker-compose up`. This will start a ZooKeeper and Kafka server

## Interacting with the Message Queues

### Apache Kafka

Time for setting up the project: 2 hours.

Kafka uses ZooKeeper. The `docker-compose` file will make sure a ZooKeeper instance is running on port 2181. A single Kafka server is instantiated on port 9092, which can be used to produce and consume messages. This Kafka server is connected to the ZooKeeper instance.

#### Producing and consuming messages

First a topic needs to be created. Without any client implementation the Kafka console scripts can be used which are provided in the `kafka_2` directory. Make sure you are in the directory or adapt the commands.

```bash
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
```

This create a topic `test`. Make sure to use the correct Kafka server port when creating the topic. There could be multiple servers running, based on the setup.

Listing all topic that are currently available.

```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Using the producer to send messages to the test topic.

```bash
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```

Starting a consumer to read all messages that have been created and listening for new messages.

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

The last two commands can be run in different shells, to see new messages coming in.

Sources:

* https://kafka.apache.org/quickstart
* https://itnext.io/how-to-install-kafka-using-docker-a2b7c746cbdc

### Apache Pulsar

Time for setting up the project: 1 hour. Without testing topics/messages.

The setup implements a dashboard that can be accessed to see information about the running Pulsar server. Two Python scripts are provided that have not been tested, due to an error with Protobuf.

```bash
$ /Users/user/anaconda3/bin/python /Users/user/code/user/uni-software_architecture/prototype/pulsarconsumer.py
Traceback (most recent call last):
  File "/Users/user/code/user/uni-software_architecture/prototype/pulsarconsumer.py", line 1, in <module>
    import pulsar
  File "/Users/user/anaconda3/lib/python3.7/site-packages/pulsar/__init__.py", line 102, in <module>
    import _pulsar
ImportError: dlopen(/Users/user/anaconda3/lib/python3.7/site-packages/_pulsar.cpython-37m-darwin.so, 2): Library not loaded: /usr/local/opt/protobuf/lib/libprotobuf-lite.22.dylib
  Referenced from: /Users/user/anaconda3/lib/python3.7/site-packages/_pulsar.cpython-37m-darwin.so
  Reason: image not found
```

Sources:

* https://pulsar.apache.org/docs/en/standalone-docker/
* https://github.com/apache/pulsar/blob/master/docker-compose/standalone-dashboard/docker-compose.yml
