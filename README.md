# streaming-05-smart-smoker
Week 5 NWMSU Streaming Data

Kellie Bernhardt
"smart smoker" (as in slow cooked food)

##Description
This producer generates messages from rows in a csv file and sends them to 3 seperate queues based upon the data provided

##Visuals
![alt text](https://github.com/krh5284/streaming-04-multiple-consumers/blob/main/screenshot.png?raw=true)

##Installation
Pika must be installed before importing. 

###Guided Producer Design 
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

###Producer Implementation Questions/Remarks
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
 

Handle User Interrupts Gracefully
Will this process be running for a while (half sec per record)?
If so, modify the code the option for the user to send a Keyboard interrupt (see earlier projects)
