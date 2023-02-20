import hashlib
import random 
import os 

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


class SecureBlackBox(object): 
    def __init__(self):
        
        # len_ = random.randint(100, 101) 
        # self._passwd = os.urandom(len_) 
        # print('init_passwd is =>', self._passwd)
        # print(type(self._passwd))


        # self.__passwd = os.urandom(len_) 

        # This is for testing
        # Below Hex string of "mypassword" 
        self.__passwd = "mypassword" 
        # print('init__passwd is =>', self.__passwd)
        # print(type(self.__passwd))


    def derivedHashPassword(self):
        # print('Derived hash __passwd is =>', self.__passwd)
        # print(type(self.__passwd))
        return hashlib.sha256(self.__passwd.encode()).hexdigest()

    def check(self, user__passwd,hashedPasswd): 
        # print('check __passwd is =>', self.__passwd)
        # print('check user__passwd is =>', user__passwd)
        print('\nUser 2 hashed password is   =>',user__passwd)
        print('Database hashed password is =>',hashedPasswd,'\n')
        # print(len(user__passwd))
        # print(len(hashedPasswd))
        
        if len(user__passwd) != len(hashedPasswd): 
            return "Error:len" 
        for i in range(len(user__passwd)): 
            if user__passwd[i] != hashedPasswd[i]: 
                return "Error:idx:%d" % i 
        return "OK" 

class callHashedPw(SecureBlackBox):
    def __init__(self):
        SecureBlackBox.__init__(self)

    def getHashPassword(self): 
        return SecureBlackBox.derivedHashPassword(self)

    def checkPw(self, thisGuess, getHashPassword):
        return SecureBlackBox.check(self, thisGuess, getHashPassword)
        
user1 = SecureBlackBox()

print('\n # OUTPUT - Testing encapsulation on SuperClass SecureBlackBox #\n')
print('_passwd seen from user1.__dict__ is =>', user1.__dict__) # calling by user1 to see Dictionary, value of _passwd is revealed
print('__passwd seen from __dict__.values() is =>', user1.__dict__.values()) # value of _passwd is revealed
print('Still can see passwd via SuperClass, which is why only passing SubClass to other programmers to use')

try:
    print('__passwd seen from user1.__passwd is =>', user1.__passwd) # value of __passwd is NOT revealed 
except AttributeError:
    print('\n\n!!!!!!!    user1.__passwd does not exist      !!!!!!! ') 
    print('Encapsulation done on Superclass. __passwd only accessible through subclass\n\n')

print(' # OUTPUT - Testing SubClass of SecureBlackBox #\n')
user2 = callHashedPw()

guess = input('User2 - Enter your password << key in [mypassword]>>: ')
# print('guess password is =>', guess)
# print('hashed guess password is =>',hashlib.sha256(guess.encode()).hexdigest())
# print('Derived hashed passwd =>', user2.getHashPassword())
if (user2.checkPw(hashlib.sha256(guess.encode()).hexdigest(),user2.getHashPassword()) == "OK"):
    print('\nPassword check is OK') 
else:
    print('\nIncorrect password for User 2')

# guess = bytes(100) 

# # print(user1.check(guess))

# while (user1.check(guess) == "Error:len"):
#     print('forming length of password')
#     guess += b'\x00' 

# # print(guess)

# for i in range(len(guess)): 
#     j = 0 
#     while (user1.check(guess) == "Error:idx:%d" % i): 
#         j += 1
#         guess = bytearray(guess) 
#         guess[i] += 1 
#         guess = bytes(guess) 
#     print(i,j)


# for i in range(len(guess)): 
#     j = 0 
#     while (user1.checkPw(guess) == "Error:idx:%d" % i): 
#         j += 1
#         guess = bytearray(guess) 
#         guess[i] += 1 
#         guess = bytes(guess) 
#     print(i,j)



# user = SecureBlackBox()
# print('__passwd is =>', user.__dict__) # {'__passwd': b'hex_str'} 
# print('__passwd is =>', user.__dict__.values())

# print(type(user.__dict__['__passwd']))


# print(user1.getHashPassword())
# print(type(user1.getHashPassword()))


# user1.__dict__.values = "sillypassword"

# print(user1.__dict__.values())

# print(user1.__passwd)

# user1.pay = 10000
# print(user1)
# print(user1.pay)


# print('\n\n\n')

# user1.len_ = 1






# # # # # Below are the all the testing done to understand Classes 
# # # # # and how to call them out
# mypassword in hex sending to determineBYTE
# determineBYTE(b'\xb1\xa5\xa3\x9c\xf6w\x02\xe4\xfcR\x9a\xaa3AhY\xc9fn\xab\x86\xa2\xf3\xc5\x87\x1c\x1e\x0b\x83\xba>R')


# print(user1.__dict__.values()) # dict_values([ ... ])
# print(type(user1.__dict__.values())) # <class 'dict_values'>

# print(type(user1.__dict__))  # <class 'dict'>
# print(len(user1.__dict__)) # 1 because there is only __passwd



# # # this gets to the generated password directly 
# print(user1.__dict__['__passwd']) # b'hex_str' i.e. the generated password
# print(type(user1.__dict__['__passwd']))  # # <class 'bytes'>

