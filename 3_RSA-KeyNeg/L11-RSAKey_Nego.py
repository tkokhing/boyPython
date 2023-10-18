# tkokhing 

import hashlib
import random
import timeit as tm
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def is_prime(n: int) -> bool:
    # This is function is modified by code found in Wiki on Primility test prime number. 
    # It is not the best prime number tester
    # The function returns when testing stuck in the loop for long duration, hence possible prime 
    start = tm.default_timer()
    """Primality test using 6k+-1 optimization."""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5

    while i ** 2 <= n:

        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
        end = tm.default_timer()
        if ((end - start) > 0.05794069999999999):
            break

    return True

def possiblePrimePair(minPrime, jumper):
    # numX is for primility test function is_prime(), where RSA ideally requires 
    #  numX to be 200 char space or 200 X 8 bits space, i.e. is 2^1600.
    # For testing purpose, numX is set lower, + 17 (or any other odd number) 
    # is to makes sure numX (always even) starts indeed as a odd number. 
    # All prime number are all odd
    step = 1000
    numX = 2**minPrime + 17 + step*jumper

    primeCounter = 0
    primeList = []

    # print('Testing prime...') 
    for i in range (numX, numX + step):
        if (is_prime(i) == True):
            primeList.insert(primeCounter,i)
            primeCounter +=1
    return primeList

def modInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    
    return u1 % m

def rabinMiller(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    s = n - 1
    t = 0
    i = 0
    while s % 2 == 0:
        s = s // 2 # s div 2
        t = t + 1
    for trial in range(0, 10):
        a = random.randrange(2, n-1)
        x = 0
        x = pow(a, s, n) # a^s mod n
        if x != 1:
            while x != (n - 1):
                if i == t - 1:
                    return False
                else:
                    return True
        else:
            i = i + 1
            x = pow(x, 2, n) # x^2 mod n

    return True

def Gen(minPrime):
    # primes number are generated in small patches for quicker testing instead of a big lump
    # it is faster and consumes lesser memory to store a big lump of primes for rabbin miller test
    # int jumper is to help to jump through the batches of gen prime
    jumper = 0

    pairPrimeFound = False
    
    print('Testing primes pair condition [p = 2q +1] using rabin miller...')
    while (pairPrimeFound!= True):
        primeList = possiblePrimePair(minPrime,jumper)

        primeListLength = len(primeList)
      
        for i in range (0,primeListLength):
            p = primeList[i]
            pResult = rabinMiller(p)

            q = primeList[i]*2 + 1
            qResult = rabinMiller(q)

            if (pResult == True and qResult == True):
                print('Prime test passed. Computed prime pair p [',p,'] and q [', q,']')
                pairPrimeFound = True
                break
            else:
                pairPrimeFound = False
                jumper += 1

    if pairPrimeFound == False:
        print('Rabin Miller Prime Test Failed! Pair primes did not meet condition [p = 2q +1]. Change value of minPrime')
        returnAnswer = False

    else:
        print('Computing now...')

        pq = p*q
        
        # below line equals to (p-1)(q-1)
        # lecture uses Greek letter Phi Φ for this number
        pqMinus = pq - p - q + 1

        e = findWholeNumber_e(pqMinus,minPrime)

        d = modInverse(e,pqMinus)

        returnAnswer = [] 
        returnAnswer.insert(0,p)
        returnAnswer.insert(1,q)
        returnAnswer.insert(2,pq)
        returnAnswer.insert(3,e)
        returnAnswer.insert(4,d)

    return returnAnswer

def findWholeNumber_e(pqMinus,minSize):
    # Since numX can change to find possible sets of primes p and q, 
    # eTest to test the criteria gcd (e, (p-1)(q-1)) = 1, 
    # by incrementing by 1 each time. If criteria met, returns e
    # minSize is used to generate of e^minSize, 
    # same size as how prime generation is based on 
    # Alternate value is e 65537, the standard e 
    e = 0
    tester = 0
    while e != 1:
        # eTest = random.randrange(2 ** ((minSize) - 1), 2 ** (minSize))
        eTest = 65537
        e = gcd(pqMinus,eTest)
        print('e test cycle: ', tester)
        # eTest += 1
        tester+=1
    
    print('e is: ', eTest)
    # eTest = 65537
    return eTest

def gcd(a, b):
    while a != 0:
        a, b = b%a, a
    return b

def constructPairKeys(n, e, d):
    # for Bob to generate his RSA keys after generating prime pairs
    keyPair = RSA.construct((n, e, d))

    return keyPair

def bobTask (p , q, n, e, d):\
    # Bob's task is to generate p, q, g based on Alice chosen minPrime
    # send back to Alice for her to check whether he is the real Bob

    # for testing diff values of m length
    # m = 1234567890 # 10
    m = 12345678901234567890 # 20
    # m = 1234567890123456789012345678901234567890 # 40
    # m = 12345678901234567890123456789012345678901234567890123456789012345678901234567890  # 80

    print('Bob generating g, p, q, random b,')
    alphaA = random.randrange(2, p-2)       
    print('Alpha: ', alphaA)
    g = 1
    i = 0
    while (g == 1):
        g = pow(alphaA, 2, p) 
        i+=1
        if g == (p -1):
            g=1

    b = random.randrange(1, q) 
    bigB = pow(g, b, p)      
    print('B: ',bigB)

    bobKeyPair = constructPairKeys(n, e, d)
    bobPubKey = bobKeyPair.publickey()

    print("\n\nBob's Public key in generated keyPair: ",)
    print("--------------------------------------")
    print(f"Public key: (n ={hex(bobPubKey.n)})")
    print(f"Public key: (e ={hex(bobPubKey.e)})")
    print("\n\nBob's Private key in generated keyPair (will not send to Alice): ",)
    print("--------------------------------------")
    print(f"Private key: (n ={hex(bobPubKey.n)})")
    print(f"Private key: (d ={hex(bobKeyPair.d)})")

    return g, bigB, b, bobPubKey 

def aliceTask(g, p, q, bigB, bobPublicKey):
    # Alice task is to check g, p and q, 
    # generate A for Bob to confirm she is Alice and encrypted message
    # generate her hashed key k1 using Bob's secret key b
    # passed to hashed key to autho channel for security channel checks
            
    aliceKeyPair = RSA.generate(1024)

    alicePubKey = aliceKeyPair.publickey()
    # alicePubKeyPEM = aliceKeyPair.exportKey()

    print("\n\nAlice's Public key in generated keyPair: ",)
    print("--------------------------------------")
    print(f"Public key: (n ={hex(alicePubKey.n)})")
    print(f"Public key: (e ={hex(alicePubKey.e)})")
    print("\n\nAlice's Private key in generated keyPair",)
    print("--------------------------------------")
    print(f"Private key: (n ={hex(alicePubKey.n)})")
    print(f"Private key: (d ={hex(aliceKeyPair.d)})")

    a = random.randrange(1, q) 
    bigA = pow(g, a, p)    
    print('A: ',bigA)
    k1 = pow(bigB, a, p)
    # print('k1 by Alice is: ',k1)
    print("------------------------------------")
    print(f"Extracting n from Bob's Public key for verification: (n={hex(bobPublicKey.n)})")
    
    n =int(bobPublicKey.n)
    # if public n is mod q 
    if (n%q == 0):
        print('n from Bob Public key, Auth_Bob and B verified and passed')

    print('\n')
    print('\n')
    msgk1 = str(k1)
    # print('k1 by Alice in str :', msgk1)
    hashedK1 = hashlib.sha256(msgk1.encode()).hexdigest()
    print('Hashed key k1 for Alice is \n', hashedK1)
    
    print('\n\nAlice sent Bob "Hi Bob, I am Alice" in encrypted form')
    aliceMsgBob = bytes(str("Hi Bob, I am Alice"), 'utf-8')
    encryptor = PKCS1_OAEP.new(alicePubKey)
    encMsg = encryptor.encrypt(aliceMsgBob)

    return bigA, aliceKeyPair, encMsg, hashedK1

def bobCheckAlice(bigA, alicePubkey, b, p, encMsg):
    # Bob is to check Alice Auth, read encrypted message, 
    # generated to common hashed based on Alice autho A to establish secure comms
    print('\n\nBob checking A and AuthAlice to see if "Alice" is the real Alice')

    decryptor = PKCS1_OAEP.new(alicePubkey)
    decrypted = decryptor.decrypt(encMsg)
    print('\nDecrypted message from Alice to Bob is: [[', decrypted.decode('utf-8'),']]')

    k2 = pow(bigA, b, p)
    msgk2 = str(k2)
    # print('Message k2 by Bob in str :', msgk2)
    hashedK2 = hashlib.sha256(msgk2.encode()).hexdigest()
    print('\nHashed key k2 for Bob is \n', hashedK2)
    
    return hashedK2

def startAutho (minPrime):
    
    returnAnswer = Gen(minPrime)

    if returnAnswer == False:
        print('Bob cannot find suitable prime pairs. End of program')

    else:
        m = 1234567890 # 10
        # m = 17000783211
        # m = 12345678901234567890 # 20
        # m = 123456789012345678901234567890 # 30
        # m = 1234567890123456789012345678901234567890 # 40
        # m = 123456789012345678901234567890123456789012345678901234567890  # 60
        # m = 1234567890123456789012345678901234567890123456789012345678901234567890  # 70
        # m = 12345678901234567890123456789012345678901234567890123456789012345678901234567890  # 80
        p = returnAnswer[0]
        q = returnAnswer[1]
        pq = returnAnswer[2]
        e = returnAnswer[3]
        d = returnAnswer[4]

        cText = pow(m,e,pq)
        pText = pow(cText,d,pq)
        
        
        print('\nFor testing whether the generated prime pair can work or not ONLY')
        print('minPrime=     ', minPrime)     
        print('p     =       ', p)     
        print('q     =       ', q)     
        print('e     =       ', e)   
        print('d     =       ', d)     
        print('p * q =       ', pq)     
        print('(p-)*(q-1) =  ', pq - p - q +1)     
        print('Ciphertext is:', cText)
        print('\n\n')
        print('Plaintext is: ',pText)
        print('Message is:   ', m)
        
        # if (m**e == True):
        if (m**e == pq):
            print('m**e == pq!!!!!!!!!!!!!')
        elif (m**e < pq):
            print('m^e is lesser than pq. No modular reduction. Attacker can recover m by simply taking the e-th root of m^e.')
        else:
            print('m^e is greater than pq. Has modular reduction')


        print('\n\n\n\nBob -> Alice: (g, p, q), B, AUTHBob')
        g, bigB, b, bobPublicKey = bobTask(p, q, pq, e, d)

        print('\n\nAlice is checking (g, p, q), B, AUTHBob, to see if "Bob" is the real Bob using her minPrime')
        bigA, alicePubkey, encMsg, hashedk1 = aliceTask(g, p, q, bigB, bobPublicKey)
                
        print('\n\nAlice sends A and AuthAlice')
        hashedk2 = bobCheckAlice(bigA, alicePubkey, b, p, encMsg)

        if (hashedk1 == hashedk2):
            print('\n\n\tHashed Keys of Alice and Bob matches. Secure connection established!!!\n\n\n')

##### Main program starts here #####

def main():
    # # minPrime refers to bits of 2, 2^minPrime, in order to gen Prime pairs
    # to save time, testing all done in low bits 
    minPrime = 31    
    print('\n\nAlice -> Bob: s = min p size: ', minPrime)
    # start to established channel authentication
    startAutho(minPrime)

    print(gcd(5,6864))
    print(4%6864)

main()