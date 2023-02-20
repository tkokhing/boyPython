""" 
This is for Q1 part 1 and 2. 
- exploitation () is from Justin


"""

import os 
import random 


def determineBYTE(testByte):
    # this function takes in Class type [Byte], 
    # test it and display the breakdown in Interger and HEX format. 
    # Return Str of Byte
    checkStr1 = ''

    print('\nByte form (in Hex) are: ') 
    i = 0

    # Byte can be only lower 4 bits (0x0f), however when display
    # it will only show 0xf (length as Str equals to 3). 
    # Thus when combining bytes together, the intepretation can go wrong
    # Hence the if-else is meant to insert 0 for len = 3
    # and return every Byte as String in proper formating  
    for byte in testByte:
        if (len(str(hex(byte))) == 3):
            hexChar = '0' + str(hex(byte))[2]
            print(hexChar, end=' ')
        else:
            hexChar = str(hex(byte))[2:]
            print(hexChar, end=' ')
        checkStr1 += hexChar

        i += 1
    checkStr1 += '\''
    print('\nTotal Bytes size is: ',i)

    return checkStr1


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


# user1 = BlackBox()
# print(' # OUTPUT #\n')
# print('_passwd seen from user1.__dict__ is =>', user1.__dict__) # calling by user1 to see Dictionary, value of _passwd is revealed
# print('_passwd seen from __dict__.values() is =>', user1.__dict__.values()) # value of _passwd is revealed
# print('_passwd seen from user1._passwd is =>', user1._passwd) # value of _passwd is revealed 


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
# guess = bytes(100) 
# # print(guess) 
# print('_passwd is =>', user1.__dict__.values())

# while (user1.check(guess) == "Error:len"):
#     guess += b'\x00' 
 
# # print(j, guess,'\n') 

# for i in range(len(guess)): 
#     j = 0 
#     while (user1.check(guess) == "Error:idx:%d" % i): 
#         j += 1
#         guess = bytearray(guess) 
#         guess[i] += 1 
#         guess = bytes(guess) 
#     print(i,j)
 
# print(i, guess,'\n') 
# print(user1.check(guess)) 

# user1.__dict__.values = "sillypassword"

# print(user1.__dict__.values())

# print(user1._passwd)

# user1.pay = 10000
# print(user1)
# print(user1.pay)


# print('\n\n\n')

# user1.len_ = 1






# # # # # Below are the all the testing done to understand Classes 
# # # # # and how to call them out
# determineBYTE(user1.__dict__['_passwd'])


# print(user1.__dict__.values()) # dict_values([ ... ])
# print(type(user1.__dict__.values())) # <class 'dict_values'>

# print(type(user1.__dict__))  # <class 'dict'>
# print(len(user1.__dict__)) # 1 because there is only _passwd



# # # this gets to the generated password directly 
# print(user1.__dict__['_passwd']) # b'hex_str' i.e. the generated password
# print(type(user1.__dict__['_passwd']))  # # <class 'bytes'>

