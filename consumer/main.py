"""
Exercise 03 — Event Consumer

Implement a RabbitMQ consumer that:
- Connects to RabbitMQ at RABBITMQ_URL env var
- Consumes messages from the "node_events" queue
- Logs each event to stdout: "EVENT: {event} | node: {node_name} | time: {timestamp}"
- Acknowledges each message after processing
"""

import json
import os
import sys
import time
import pika


def main():
    rabbitmq_url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    params = pika.URLParameters(rabbitmq_url)

    delay = 1
    max_delay = 30

    while True:
        try:
            print("Connecting to RabbitMQ...", flush=True)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue="node_events", durable=True)
            delay = 1

            print("Consumer ready. Waiting for messages...", flush=True)

            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body.decode("utf-8"))
                    event = data.get("event")
                    node_name = data.get("node_name")
                    timestamp = data.get("timestamp")
                    print(f"EVENT: {event} | node: {node_name} | time: {timestamp}", flush=True)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    print(f"Error processing message: {e}", flush=True)
                    ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(
                queue="node_events",
                on_message_callback=callback,
                auto_ack=False,
            )
            channel.start_consuming()


        except (pika.exceptions.AMQPConnectionError, pika.exceptions.StreamLostError) as e:
            print(f"RabbitMQ connection error ({e}). Retrying in {delay}s...", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, max_delay)
        except KeyboardInterrupt:
            print("Consumer stopping...", flush=True)
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error ({e}). Retrying in {delay}s...", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, max_delay)


if __name__ == "__main__":
    main()

