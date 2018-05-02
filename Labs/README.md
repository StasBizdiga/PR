# PR
Network Programming / Programarea in Retea
## [Lab1](https://github.com/StasBizdiga/PR)
Setting up the Repository
## [Lab2-3](https://github.com/StasBizdiga/PR/tree/master/Labs/src/Lab2-3)
Metrics Aggregator - a client with parallel threading superpowers
## [Lab4](https://github.com/StasBizdiga/PR/tree/master/Labs/src/Lab4)
Email client with SMTP and IMAP featuring an amazingly designed GUI
## [Lab5](https://github.com/StasBizdiga/PR/tree/master/Labs/src/Lab5)
Client-Server App - TCP communication
### Protocol Specification
#### General Information
* Language: Python
* Libraries: socket,threading,regex,random
* Concurrent Processing: Creating a new thread for each connected client
* Code architecture: 
  * server.py - the code for server base
  * client.py - client functionality 
  * fncs.py - the functions the server uses for client commands
  
#### Message Format
The messages the server receives should conform to the next features:
* They should be alphanumeric, i.e. they can contain `A-Za-z0-9` 
* The commands start with `/`
* The commands that require parameters, accept them using spaces. `example: /hello text`
* If a command requires `n` parameters, but the message contains `< n`, an informative message is displayed.
* If a command requires `n` parameters, but the message contains `n+m` parameters, the `m` ones are ignored.
* If the command is invalid, the answer is informative.
* If the message contains non alphanumeric characters, the connection is interrupted.

#### Server Commands
```
/help - displays this list of available commands
/hello <text> - returns the text that was sent as param
/prime <int> - tells if the given number is prime
/area <int> <int> - tells the area of a rect with given x,y params
/answer - responds to your most interested question with an 'yes' or 'no' 
/joke - tells a python joke
/exit - closes connection
```
#### Example Responses
```
>>>
<<<Write a command! Do you need '/help'?
>>>/help
<<<
===============
=== h e l p ===
===============
/help - displays this list of available commands
/hello <text> - returns the text that was sent as param
/prime <int> - tells if the given number is prime
/area <int> <int> - tells the area of a rect with given x,y params
/answer - responds to your most interested question with an 'yes' or 'no' 
/joke - tells a python joke
/exit - closes connection
===============
>>>/hello friend
<<<friend
>>>/prime 13 
<<<13 is a prime number!
>>>/area 20 11 
<<<220
>>>/answer
<<<yes
>>>/joke
<<<Never is often better than right now.
>>>/exit
<<<Closing connection...
```

