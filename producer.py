import pika
import sys
import webbrowser
import csv
import time

# Function to offer to open the RabbitMQ Admin website
def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # Create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # Use the connection to create a communication channel
        ch = conn.channel()
        # Use the channel to declare a durable queue
        ch.queue_declare(queue=queue_name, durable=True)
        # Use the channel to publish a message to the queue
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # Print a message to the console for the user
        print(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # Close the connection to the server
        conn.close()

# Function to read a CSV file to a list
def read_csv_to_queue(filename: str):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            time_stamp = row[0]
            smoker_temp = row[1]
            food_a_temp = row[2]
            food_b_temp = row[3]
            
            # Send to queue based on data returned
            if smoker_temp:
                message = f"{time_stamp},smoker,{float(smoker_temp)}"
                send_message("localhost", "01-smoker", message)
            if food_a_temp:
                message = f"{time_stamp},food-A,{float(food_a_temp)}"
                send_message("localhost", "02-food-A", message)
            if food_b_temp:
                message = f"{time_stamp},food-B,{float(food_b_temp)}"
                send_message("localhost", "03-food-B", message)
                
            time.sleep(1)  # Wait 30 seconds between messages
            print(f"Sent: {message}. Hit CTRL-C to stop.")

# Standard Python idiom to indicate main program entry point
if __name__ == "__main__":  
    # Ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site()
    read_csv_to_queue('smoker-temps.csv')
