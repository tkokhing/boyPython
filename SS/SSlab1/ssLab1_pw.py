""" 
This is for Q1 part 1 and 2. 

"""

import os 
import random 

class BlackBox(object): 
    def __init__(self):
        len_ = random.randint(100, 1000) 
        self.__passwd = os.urandom(len_) # generating system password
     
    def check(self, user_passwd): 
        if len(user_passwd) != len(self.__passwd): 
            return "Error:len" 
        for i in range(len(user_passwd)): 
            if user_passwd[i] != self.__passwd[i]: 
                return "Error:idx:%d" % i 
        return "OK" 

def exploitSuperClass(testClass):   
    guess = bytes(100) 
    # covert channel to determine password length
    while (testClass.check(guess) == "Error:len"):
        guess += b'\x00' 
    
    for i in range(len(guess)): 
        j = 0 
        while (testClass.check(guess) == "Error:idx:%d" % i): 
            j += 1
            guess = bytearray(guess) 
            guess[i] += 1 
            guess = bytes(guess) 

    print('Password in Hex is =>' , guess,'\n') 
    return guess

############   Q1 PART 1   ############   
# user1 = BlackBox()
# print(' # OUTPUT #\n')
# print('_passwd seen from user1.__dict__ is =>', user1.__dict__) # calling by user1 to see Dictionary, value of _passwd is revealed
# print('_passwd seen from __dict__.values() is =>', user1.__dict__.values()) # value of _passwd is revealed
# print('_passwd seen from user1._passwd is =>', user1._passwd) # value of _passwd is revealed 
############   Q1 PART 1   ############   


############   MAIN PROGRAM STARTS HERE   ############   
print('\n # OUTPUT - Testing exploitation on SuperClass BlackBox #\n')
testStatus = True
user1 = BlackBox() 

while testStatus:
    if (user1.check(exploitSuperClass(user1)) == "OK"):
        print('SuperClass exploitation success')
        testStatus = False
    else:
        print('SuperClass exploitation failed')