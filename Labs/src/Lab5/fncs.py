import random

def help_me():
    return help_description.encode('utf-8')

def hello(word):
    return word.encode('utf-8')
    
def is_prime(n):
    n = int(n)
    if n > 1:
        for i in range(2,n):
            if (n % i) == 0:
                ans = str(n) + " isn't a prime number!\n"
                ans = ans + str(i) + " * " + str(n//i) + " = " + str(n)
                break
            else:
                ans = str(n) + " is a prime number!\n"
    else:
        ans = str(n) + " isn't a prime number!\n"   
    return ans.encode('utf-8')

def rect_area(x,y):
    ans=int(x)*int(y)
    return bytes(str(ans),'utf-8')
    
def answer():
    return random.choice(yn).encode('utf-8')
    
def joke():
    return random.choice(jokelist).encode('utf-8')
    
    
help_description = \
"""
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
"""

yn = ['yes','no']

jokelist = \
[
'Beautiful is better than ugly.',
'Simple is better than complex.',
'Flat is better than nested.',
'Sparse is better than dense.',
'Special cases aren\'t special enough to break the rules.',
'Errors should never pass silently.',
'In the face of ambiguity, refuse the temptation to guess.',
'There should be one-- and preferably only one --obvious way to do it.',
'Now is better than never.',
'Never is often better than right now.',
'If the implementation is hard to explain, it\'s a bad idea.',
'If the implementation is easy to explain, it may be a good idea.',
'Namespaces are one honking great idea -- let\'s do more of those!'
]