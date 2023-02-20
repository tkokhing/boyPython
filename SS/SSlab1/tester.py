import hashlib
import random 
import os 

# len_ = random.randint(100, 1000) 
# passwd = os.urandom(len_) 

# print(passwd)
# print('\n')
# print(str(passwd))
#     # derived hashed of private __password
#     # created for calling from SubClass, so atrribute __passwd is not known
# # passwd = random.randrange(0, len_)
# print('\n')

# guess = bytes(0) 
# print(guess)
# print(hashlib.sha256((str(guess)).encode()).hexdigest())

# guess += b'\x00' 
# print(guess)
# print(hashlib.sha256((str(guess)).encode()).hexdigest())

# guess += b'\x00' 
# print(guess)
# print(hashlib.sha256((str(guess)).encode()).hexdigest())

# guess += b'\x00' 
# print(guess)
# print(hashlib.sha256((str(guess)).encode()).hexdigest())
# # print(hashlib.sha256(passwd)).hexdigest()

# print(hashlib.sha256(passwd.encode()).hexdigest())

def formPasswdTestStr():
    # alpha1 = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz'
    # alpha2 = ";':-="
    # alpha3 = '`~!@#$%^&*()_+[]\}{|",./<>?'

    # alpha = alpha1 + alpha2 + alpha3

    alpha = 'ABCDEF'
    str_in = "U37"
    # str_in = "BTWQI"
    n = len(str_in)
    str_test = []

    print(n)

    for i in range (n):
        print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        for letter in alpha:
            print(letter)
            print(i)

            str_test.insert(i, letter)
            print(str_test)
            # print(hashlib.sha256((str_test).encode()).hexdigest())



def main():
    formPasswdTestStr()

main()