""" 
This is for Q1 part 3. 

"""
import hashlib
import random 
import os 

class SecureBlackBox(object): 
    def __init__(self):
        len_ = random.randint(100, 1000) 
        self.__passwd = os.urandom(len_) # generating system password

    # user_passwd is compared with the hashed of system password 
    def check(self, user_passwd): 
        if len(user_passwd) != len(self.derivedHashPassword()): 
            return "Error:len" 
        for i in range(len(user_passwd)): 
            if user_passwd[i] != self.__passwd[i]: 
                return "Error:idx:%d" % i 
        return "OK" 

    # derived hashed of private __password
    # created for calling from SubClass, so atrribute __passwd is not known
    def derivedHashPassword(self):
        return hashlib.sha256(str(self.__passwd).encode()).hexdigest()

# With SuperClass made private, 
# these two functions are for calling SuperClass functions, not its attributes  
class callHashedPw(SecureBlackBox):
    def __init__(self):
        SecureBlackBox.__init__(self)

    def getHashPassword(self): 
        return SecureBlackBox.derivedHashPassword(self)

    def checkPw(self, thisGuess):
        return SecureBlackBox.check(self, thisGuess)

def exploitSuperClass(testClass):   
    guess = bytes(0) 
    
    while (testClass.check(guess) == "Error:len"):
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        guess += b'\x00' 
    
    # print(j, guess,'\n') 

    for i in range(len(guess)): 
        j = 0 
        while (testClass.check(guess) == "Error:idx:%d" % i): 
            j += 1
            guess = bytearray(guess) 
            guess[i] += 1 
            guess = bytes(guess) 
        print(i,j)

    print(i, guess,'\n') 

    return guess


def exploitSubClass(testClass):   

    guess = bytes(0) 
    # covert channel to determine password length
    # this is irrelevant because pw has been hashed i.e. 64 Bytes length
    while (testClass.checkPw(guess) == "Error:len"):
        guess += b'\x00' 
    
    for i in range(len(guess)): 

        # using the same logic as generation of system passwd
        len_ = random.randint(100, 1000) 
        testPasswd = os.urandom(len_) 

        try:
            hashedGuess = (hashlib.sha256((str(testPasswd)).encode()).hexdigest())
            while (testClass.checkPw(hashedGuess) == "Error:idx:%d" % i): 
                hashedGuess = bytearray(bytes.fromhex(hashedGuess)) 
                hashedGuess[i] += 1 
                hashedGuess = bytes(hashedGuess) 
        except Exception as m:
            # This is the key to hashing password coz actual length of password is unknown
            print('Max hash length reached, error is raised => ', m)

    print('Password on test is =>' , testPasswd,'\n') 
    return hashedGuess

############   MAIN PROGRAM STARTS HERE   ############   
print(' # OUTPUT - Testing exploitation on SubClass of SecureBlackBox #\n')
testStatus = True
user2 = callHashedPw()

while testStatus:
    if (user2.checkPw(exploitSubClass(user2)) == "OK"):
        print('SubClass exploitation success')
        testStatus = False
    else:
        print('SubClass exploitation failed')