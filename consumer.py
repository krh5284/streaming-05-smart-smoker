import pika
import sys
import time
from collections import deque

# Store temperature readings for each queue
smoker_history = deque(maxlen=5)
food_a_history = deque(maxlen=20)
food_b_history = deque(maxlen=20)

# Alert thresholds
ALERT_THRESHOLD_SMOKER = 15  # degrees
ALERT_THRESHOLD_FOOD = 1  # degrees

# Define a callback function to be called when a message is received
def callback(ch, method, properties, body):
    """Define behavior on getting a message."""
    # Decode the binary message body to a string
    message = body.decode()
    print(f" [x] Received {message}")

    # Extract temperature from the message, ignoring the first column
    try:
        _, temp_type, temperature = message.split(",")
        temperature = float(temperature)
    except (ValueError, IndexError):
        print(" [!] Invalid message format or temperature reading.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    queue_name = method.routing_key
    if queue_name == "01-smoker":
        smoker_history.append(temperature)
        if len(smoker_history) == 5:
            if (smoker_history[0] - smoker_history[-1]) >= ALERT_THRESHOLD_SMOKER:
                print(" [ALERT] 01-smoker: Temperature dropped by 15 degrees or more in the last 5 readings.")
    elif queue_name == "02-food-A":
        food_a_history.append(temperature)
        if len(food_a_history) == 20:
            if max(food_a_history) - min(food_a_history) <= ALERT_THRESHOLD_FOOD:
                print(" [ALERT] 02-food-A: Temperature change is 1 degree or less in the last 20 readings.")
    elif queue_name == "03-food-B":
        food_b_history.append(temperature)
        if len(food_b_history) == 20:
            if max(food_b_history) - min(food_b_history) <= ALERT_THRESHOLD_FOOD:
                print(" [ALERT] 03-food-B: Temperature change is 1 degree or less in the last 20 readings.")

    # Simulate work by sleeping for a while
    time.sleep(1)

    # When done with task, tell the user
    print(" [x] Done.")
    
    # Acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main(hn):
    """Process messages from multiple queues."""
    try:
        # Create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))
        channel = connection.channel()

        # Declare the durable queues
        channel.queue_declare(queue="01-smoker", durable=True)
        channel.queue_declare(queue="02-food-A", durable=True)
        channel.queue_declare(queue="03-food-B", durable=True)

        # Set the QoS level to 1 to limit the number of messages being processed concurrently
        channel.basic_qos(prefetch_count=1)

        # Configure the channel to listen on specific queues with the shared callback
        channel.basic_consume(queue="01-smoker", on_message_callback=callback)
        channel.basic_consume(queue="02-food-A", on_message_callback=callback)
        channel.basic_consume(queue="03-food-B", on_message_callback=callback)

        # Print a message to the console for the user
        print(" [*] Ready for work on queues 01-smoker, 02-food-A, and 03-food-B. To exit press CTRL+C")

        # Start consuming messages
        channel.start_consuming()

    except Exception as e:
        print(f"ERROR: something went wrong.")
        print(f"The error says: {e}")
    except KeyboardInterrupt:
        print(" User interrupted continuous listening process.")
    finally:
        print("Closing connection. Goodbye.\n")
        if connection.is_open:
            connection.close()

# Standard Python idiom to indicate main program entry point
if __name__ == "__main__":
    main("localhost")
