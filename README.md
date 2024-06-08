# streaming-05-smart-smoker
Week 5 NWMSU Streaming Data

Kellie Bernhardt
"smart smoker" (as in slow cooked food)

## Description
The producer generates messages from rows in a csv file and sends them to 3 seperate queues based upon the data provided

The consumer monitors the 3 queues and generates alerts if:
    1. the smoker temperature decreases by 15 degrees or more over 2.5 minutes (5 readings)
    2. either food-A or food-B temperature change is 1 degree or less for the last 10 minutes (20 readings)
## Visuals

![alt text](https://github.com/krh5284/streaming-05-smart-smoker/blob/main/screenshot.png)

![alt text](https://github.com/krh5284/streaming-05-smart-smoker/blob/main/consumer_smoker_screenshot.png)

![alt text](https://github.com/krh5284/streaming-05-smart-smoker/blob/main/consumer_food_screenshot.png)

## Installation
Pika must be installed before importing. 

### Guided Producer Design 
If this is the main program being executed (and you're not importing it for its functions),
We should call a function to ask the user if they want to see the RabbitMQ admin webpage.
We should call a function to begin the main work of the program.
As part of the main work, we should
Get a connection to RabbitMQ, and a channel, delete the 3 existing queues (we'll likely run this multiple times), and then declare them anew. 
Open the csv file for reading (with appropriate line endings in case of Windows) and create a csv reader.
For data_row in reader:
[0] first column is the timestamp - we'll include this with each of the 3 messages below
[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
[2] Channe2 = Food A Temp --> send to message queue "02-food-A"
[3] Channe3 = Food B Temp --> send to message queue "02-food-B"
Send a tuple of (timestamp, smoker temp) to the first queue
Send a tuple of (timestamp, food A temp) to the second queue
Send a tuple of (timestamp, food B temp) to the third queue 
Create a binary message from our tuples before using the channel to publish each of the 3 messages.
Messages are strings, so use float() to get a numeric value where needed
 Remember to use with to read the file, or close it when done.

### Producer Implementation Questions/Remarks
Will you use a file docstring at the top? Hint: yes
Where do imports go? Hint: right after the file/module docstring
After imports, declare any constants.
After constants, define functions.
Define a function to offer the RabbitMQ admin site, use variables to turn it off temporarily if desired.
Define a main function to
connect,
get a communication channel,
use the channel to queue_delete() all 3 queues 
use the channel to queue_declare() all 3 queues
open the file, get your csv reader, for each row, use the channel to basic_publish() a message
Use the Python idiom to only call  your functions if this is actually the program being executed (not imported). 
If this is the program that was called:
call your offer admin function() 
call your main() function, passing in just the host name as an argument (we don't know the queue name or message yet)
### Consumer Design
How many connections do you need? Hint: Just one connection per consumer.
Create a connection object. 
How man communication channels do you need? Hint: Just one communication channel per consumer.
How many queues do you need: Hint: see the queue names in the problem description. How many queue names are there?
Call channel.queue_declare() once for each queue.
Provide the appropriate arguments as you've done before - see prior examples.
Declare different callback functions
smoker_callback(),
foodA_callback(),
foodB_callback()
You can have one per consumer, or three if you're implementing a single consumer.
Each callback has the same signature and general approach as you've seen before.
More about each callback later - for now, just "stub it in" and we'll come back to finish the callbacks later. 
This is common - we build code more like an outline - from the outside in.
We don't write code from left to right like an essay.  Just make a callback that doesn't kill your program - defer the logic until later.
Set up a basic consume once for each queue. 
Call channel.basic_consume() once for each queue.
Follow prior examples.
set auto_ack to False - we've explored both options, but we want to process the message first, before we acknowledge it and have it removed from the queue. 
set on_message_callback to the name of the callback function.
Important: assigning the function does NOT include the parenthesis.
If you add parenthesis after the name, you'll accidentally CALL the function instead of assigning it (don't do this).
Call channel.start_listening() just once - the configured communication channel will listen on all three configured queues. 
### Guided Consumer Implementation
Consumer Implementation Questions/Remarks
Will you use a file docstring at the top? Hint: yes
Where do imports go? Hint: right after the file/module docstring
After imports, declare any constants. 
After constants, define functions - define your callback function(s) here.
Use the examples to create each callback. It'll have the same arguments. For now, just have a callback function:
acknowledge the message was received and processed
Define a main() function to continuously listen for task messages on a named queue.
In this main() function:
create a blocking connection to the RabbitMQ server
use the connection to create a communication channel
use the channel to queue_delete() each queue
use the channel to queue_declare() each queue
use channel.basic_consume() once for each queue. Use the call to configure the channel to listen to a named queue and assign a callback function
print a message to the console for the user that it's ready to begin (and maybe, how to exit the long-running process).
finally, use channel.start_consuming() to start consuming messages via the communication channel
Use the Python idiom to only call  your main() function only if this is actually the program being executed (not imported). 
If this is the program that was called:
call your main() function, passing in just the host name as an argument, and the name of each queue this consumer monitors

### Handle User Interrupts Gracefully
Will this process be running for a while (half sec per record)?
If so, modify the code the option for the user to send a Keyboard interrupt (see earlier projects)
