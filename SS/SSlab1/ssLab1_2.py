import hashlib
import random 
import os 

class SecureBlackBox(object): 
    def __init__(self):
        # commented out the provided codes
        # len_ = random.randint(100, 1000) 
        # self._passwd = os.urandom(len_) 

        # For testing, defined the database password
        self.__passwd = "mypassword" 

    # derived hashed of private __password
    # created for calling from SubClass, so atrribute __passwd is not known
    def derivedHashPassword(self):
        return hashlib.sha256(self.__passwd.encode()).hexdigest()

    # the logic of using string length for comparison is untouch
    # modified by adding one parameter hashedPasswd for comparison
    def check(self, user__passwd,hashedPasswd): 
        print('\nUser 2 hashed password is   =>',user__passwd)
        print('Database hashed password is =>',hashedPasswd,'\n')
        
        if len(user__passwd) != len(hashedPasswd): 
            return "Error:len" 
        for i in range(len(user__passwd)): 
            if user__passwd[i] != hashedPasswd[i]: 
                return "Error:idx:%d" % i 
        return "OK" 

class callHashedPw(SecureBlackBox):
    def __init__(self):
        SecureBlackBox.__init__(self)

    # With SuperClass made private, 
    # these two functions are for calling SuperClass functions, not its attributes  
    def getHashPassword(self): 
        return SecureBlackBox.derivedHashPassword(self)

    def checkPw(self, thisGuess, getHashPassword):
        return SecureBlackBox.check(self, thisGuess, getHashPassword)

def exploitSuperClass(testClass):   
    guess = bytes(100) 
    # print(guess) 
    print('_passwd is =>', testClass.__dict__.values())

    while (testClass.check(guess,testClass.derivedHashPassword()) == "Error:len"):
        guess += b'\x00' 
    
    # print(j, guess,'\n') 

    for i in range(len(guess)): 
        j = 0 
        while (testClass.check(guess,testClass.derivedHashPassword()) == "Error:idx:%d" % i): 
            j += 1
            guess = bytearray(guess) 
            guess[i] += 1 
            guess = bytes(guess) 
        print(i,j)

    print(i, guess,'\n') 

    return guess


user1 = SecureBlackBox()

print('\n # OUTPUT - Testing encapsulation on SuperClass SecureBlackBox #\n')
print('_passwd seen from user1.__dict__ is =>', user1.__dict__) # calling by user1 to see Dictionary, value of _passwd is revealed
print('__passwd seen from __dict__.values() is =>', user1.__dict__.values()) # value of _passwd is revealed
print('Above showed that passwd can be seen via SuperClass using DICT, which is why only passing SubClass to other programmers to use')

try:
    print('__passwd seen from user1.__passwd is =>', user1.__passwd) # value of __passwd is NOT revealed 
except AttributeError:
    print('\n\n!!!!!!!    user1.__passwd does not exist      !!!!!!! ') 
    print('Encapsulation done on Superclass\n\n')

if (user1.check(exploitSuperClass(user1)) == "OK"):
    print('SuperClass exploitation success')
else:
    print('SuperClass exploitation failed')

print(' # OUTPUT - Testing SubClass of SecureBlackBox #\n')
user2 = callHashedPw()

guess = input('User2 - Enter your password << key in [mypassword]>>: ')

if (user2.checkPw(hashlib.sha256(guess.encode()).hexdigest(),user2.getHashPassword()) == "OK"):
    print('\nPassword check is OK') 
else:
    print('\nIncorrect password for User 2')


# user1 = BlackBox() 
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