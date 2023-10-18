#!/usr/bin/env python
# Skeleton for Security Tools Lab 1 - Simple ciphers
# Student ID:10***92
# StudentName: tkokhing

import binascii as b
from encodings import utf_8
from typing import Dict, List
from pickle import FALSE, TRUE
import argparse
import json
import random
import requests
 
# this function takes in Class type [BYTE], 
# return List of Bytes in Interger  
def determineBYTE(testByte):
    
    intMsgStrList =[]
    for byte in testByte:
        intMsgStrList.append(int(byte))

    return intMsgStrList

def cycleChar(MsgList):
    OFFSET = 32
    CYCLELENGTH = 128 - OFFSET
    saveFile = open('000PossibleMsgList.txt', 'w')

    # cycle through the ASCII range
    for i in range (CYCLELENGTH):
        possibleSentence = ''
        possibleSentence = formSentence(i, MsgList, OFFSET, CYCLELENGTH, TRUE)
        saveFile.write('----------------------\n' + 'KEY ID: ' + str(i) + '\n')        
        saveFile.write(possibleSentence)
        saveFile.write('\n----------------------\n\n') 
        possibleSentence = formSentence(i, MsgList, OFFSET, CYCLELENGTH, FALSE)
        saveFile.write('----------------------\n' + 'KEY ID: ' + str(i) + '\n')        
        saveFile.write(possibleSentence)
        saveFile.write('\n----------------------\n\n') 

    saveFile.close()

def formSentence(i, MsgList, OFFSET, CYCLELENGTH, MODE):
    challengeSentence = ''

    if (MODE==TRUE):
        for intLetter in MsgList:
            eachChar = chr((i + intLetter - OFFSET)%CYCLELENGTH + OFFSET ) 
            challengeSentence += eachChar
    else:
        for intLetter in MsgList:
            eachChar = hex((i + intLetter - OFFSET)%CYCLELENGTH + OFFSET ) 
            challengeSentence += eachChar[2:]

    return challengeSentence

def challengeSentence(i, MsgList):
    challengeSentence = ''

    for intLetter in MsgList:
        eachChar = hex((i + intLetter)) 
        challengeSentence += eachChar[2:]

    return challengeSentence


# this function computes the freq of letters 
def genCharFreqDict(numList):

    repeatedNumList = []
    numCountList = []
    maxNumList = []
    sorted_numList = sorted(numList)

    # compute length for loop
    listLength = len(sorted_numList)
    # Added a trailing impossible number at the end for completing entire loop x+1
    sorted_numList.insert(-1,1000)

    numCounter = 1
    repeatedNumCounter = 0 
    # t = 0

    for i in range (0,listLength):
        # if (x  == (x+1)), add counter
        if sorted_numList[i] == sorted_numList[i+1]:
            # if that number is not inside repeatedNumList, it is the first occurrance 
            # write number into repeatedNumList
            # start counting repeatedNumCounter for indexing List purpose
            # add 1 to numCounter
            if sorted_numList[i] not in repeatedNumList:
                repeatedNumList.insert(repeatedNumCounter, sorted_numList[i])
                repeatedNumCounter += 1
                numCounter += 1
        
            # if that word is already inside repeatedNumList, 
            # add numCounter
            else:
                numCounter += 1
                
        # if (x  != (x+1)), 2 possibilities 
        #       Either end of repeated words, 
        #       or start of solo new word 
        else: 
            # if there are already same number found
            # write to total count of the same number into numCoutlist [] 
            # at position by repeatedNumCounter
            # once written, reset numCounter to 1 for next use

            if numCounter >= 2: 
                repeatedNumList.insert(repeatedNumCounter, sorted_numList[i])
                numCountList.insert(repeatedNumCounter, numCounter)
                numCounter = 1

            # sequence of single word, reset numCounter to prepare for new repeated number
            else: 
                repeatedNumList.insert(repeatedNumCounter, sorted_numList[i])
                numCountList.insert(repeatedNumCounter, numCounter)
                repeatedNumCounter += 1
                numCounter = 1

    for x in range (0, repeatedNumCounter):
        maxNumList.insert(x,[numCountList[x], repeatedNumList[x], numCountList[x]/listLength*100]) 
    # Sort by highest repeating numbers that are generated, 
    # to make inserted dummy number is at the -1 and pop it out
    # minus repeatedNumCounter
    maxNumList.sort(reverse=True)
    maxNumList.pop(-1)
    repeatedNumCounter -=1

    print('\n','Total count of Hex Char is:', repeatedNumCounter )
    print('(No. )   Hex Char :  [# times]  [ freq %  ]')
    for i in range (0,repeatedNumCounter):
        print('({0:^4d})'. format(i+1),' {0:^10}:'. format(hex(maxNumList[i][1])), ' [{0:^7d}]'. format(maxNumList[i][0]), ' [{0:^4f}]'. format(maxNumList[i][2]))
 
    input('Freq of letters generated. Press ENTER to continue.')
 
    hexFreqDict : Dict[str, List['[{:.4f}]'.format(float)]] = { hex(maxNumList[i][1]): [maxNumList[i][0], maxNumList[i][2]] for i in range (repeatedNumCounter)} 
    return hexFreqDict


def solveSubstituition(hex_val):
    
    # this char groupings are created based on analysis of 
    # freq of letters
    charGrp1 = " "
    charGrp2 = "e"
    charGrp3 = "t"
    charGrp4 = "o"
    charGrp5 = "a"
    charGrp6 = "h"
    charGrp7 = "r"
    charGrp8 = "n"
    charGrp9 = "d"
    charGrp10 = "i"
    charGrp11 = "s"
    charGrp12 = "l"
    charGrp13 = "w"
    charGrp14 = "g"
    charGrp15 = "u"
    charGrp16 = ","
    charGrp17 = "\\r\\n"
    charGrp18 = "y"
    charGrp19 = "c"
    charGrp20 = "m"
    charGrp21 = "f"
    charGrp22 = "p"
    charGrp23 = "."
    charGrp24 = "b"
    charGrp25 = "v"
    charGrp26 = "k"
    charGrp27 = "-"
    charGrp28 = "j"
    charGrp29 = "'"
    charGrp30 = "?"
    charGrp31 = "q"

    answer = bytearray.fromhex(hex_val[2:])

    numList = determineBYTE(answer)

    generatedCharFreqDict = genCharFreqDict(numList)

    saveFile = open('PossibleSentence.txt', 'w')

    sentenceToWrite = '' 

    intMsgStrList =[]

    for hexString in numList:

        testFreq = generatedCharFreqDict[(hex(hexString))][1]
        # these series of comparison is 
        # to breakdown the freq of characters and perform substituition
        if (testFreq > 15):
            tempLetter = charGrp1

        elif (testFreq < 15 and testFreq > 10):
            tempLetter = charGrp2

        elif (testFreq < 10 and testFreq > 7):
            tempLetter = charGrp3

        elif (testFreq < 7 and testFreq > 6.3):
            tempLetter = charGrp4

        elif (testFreq < 6.3 and testFreq > 6.1):
            tempLetter = charGrp5

        elif (testFreq < 6.1 and testFreq > 5.8):
            tempLetter = charGrp6

        elif (testFreq < 5.8 and testFreq > 4.8):
            tempLetter = charGrp7

        elif (testFreq < 4.8 and testFreq > 4.3):
            tempLetter = charGrp8

        elif (testFreq < 4.3 and testFreq > 4):
            tempLetter = charGrp9

        elif (testFreq < 4 and testFreq > 3.8):
            tempLetter = charGrp10

        elif (testFreq < 3.8 and testFreq > 3.7):
            tempLetter = charGrp11

        elif (testFreq < 3.7 and testFreq > 3.2):
            tempLetter = charGrp12

        elif (testFreq < 3.2 and testFreq > 2.3):
            tempLetter = charGrp13

        elif (testFreq < 2.3 and testFreq > 2.05):
            tempLetter = charGrp14

        elif (testFreq < 2.05 and testFreq > 2):
            tempLetter = charGrp15

        elif (testFreq < 2 and testFreq > 1.9):
            tempLetter = charGrp16

        elif (testFreq < 1.9 and testFreq > 1.8):
            tempLetter = charGrp17

        elif (testFreq < 1.8 and testFreq > 1.5):
            tempLetter = charGrp18

        elif (testFreq < 1.5 and testFreq > 1.45):
            tempLetter = charGrp19

        elif (testFreq < 1.45 and testFreq > 1.3):
            tempLetter = charGrp20

        elif (testFreq < 1.3 and testFreq > 1.23):
            tempLetter = charGrp21

        elif (testFreq < 1.23 and testFreq > 1.2):
            tempLetter = charGrp22

        elif (testFreq < 1.2 and testFreq > 1):
            tempLetter = charGrp23

        elif (testFreq < 1 and testFreq > 0.8):
            tempLetter = charGrp24

        elif (testFreq < 0.8 and testFreq > 0.65):
            tempLetter = charGrp25

        elif (testFreq < 0.65 and testFreq > 0.6):
            tempLetter = charGrp26

        elif (testFreq < 0.6 and testFreq > 0.3):
            tempLetter = charGrp27

        elif (testFreq < 0.3 and testFreq > 0.09):
            # both j and ' each having 5 out of 5000 
            # if previous char is SPACE, then insert j
            if sentenceToWrite[-1] == charGrp1:
                tempLetter = charGrp28
            # if not space, insert '. I.e. grandmother's 
            else:
                tempLetter = charGrp29

        elif (testFreq < 0.09 and testFreq > 0.06):
            tempLetter = charGrp30

        elif (testFreq < 0.06 and testFreq > 0.03):
            tempLetter = charGrp31


        sentenceToWrite += tempLetter
        intMsgStrList.append(tempLetter)

        saveFile.write('----------------------\n' + 'Patience, work out the puzzle' +'\n')        
        saveFile.write(sentenceToWrite)
        saveFile.write('\n----------------------\n\n') 

    saveFile.close()

    return (''.join(intMsgStrList))




def xorString(s1,s2):
    """ 
        XOR two strings with each other, return result as string
    """
    rval = [ord(a) ^ ord(b) for a,b in zip(s1,s2)]
    return ''.join([chr(r) for r in rval])


def resolvePlainChallenge():
    """
        Solution of plain challenge
    """
    url = "http://{}:{}/".format(IP, PORT)
    headers = {'Content-Type': 'application/json'}

    r = requests.get(url + 'challenges/plain')
    data = r.json()
    print("[DEBUG] Obtained challenge ciphertext: %s with len %d" % (data['challenge'], len(data['challenge'])))

    # TODO: Add a solution here (conversion from hex to ascii will reveal that the result is in a human readable format)
    a = data['challenge'][2:]
    s = bytearray.fromhex(a).decode()

    payload = {'cookie': data['cookie'], 'solution': s}
    print("[DEBUG] Submitted solution is:")
    print(json.dumps(payload, indent=4, separators=(',', ': ')))

    r = requests.post(url + 'solutions/plain', headers=headers, data=json.dumps(payload))
    print("[DEBUG] Obtained response: %s" % r.text)


def resolveCaesarChallenge():
    """
        Solution of caesar challenge
    """
    url = "http://{}:{}/".format(IP, PORT)
    headers = {'Content-Type' : 'application/json'}

    r = requests.get(url + 'challenges/caesar')
    data = r.json()
    print("[DEBUG] Obtained challenge ciphertext: %s with len %d" % (data['challenge'], len(data['challenge'])))

    # TODO: Add a solution here (conversion from hex to ascii will reveal that the result is in a human readable format)
    
    hex_val = data['challenge']
  
    challengeString = bytearray.fromhex(hex_val[2:])  
   
    intMsgList = determineBYTE(challengeString)

    cycleChar(intMsgList)

    inNum = int(input('Visually inspect output file [000PossibleMsgList.txt]. Enter KEY ID #: '))
    OFFSET = 32
    CYCLELENGTH = 128 - OFFSET
    decryptHexSentence = formSentence(inNum, intMsgList, OFFSET, CYCLELENGTH, FALSE)
    decryptHexSentence = decryptHexSentence.replace('6d6a','0d0a') # # tackle CRLF
    
    decryptsource = bytearray.fromhex(decryptHexSentence).decode()
    solution = decryptsource

    print(solution) # # 
 
    payload = { 'cookie' : data['cookie'], 'solution' : solution}
    print("[DEBUG] Submitted solution is:")
    print(json.dumps(payload, indent=4, separators=(',', ': ')))

    r = requests.post(url+'solutions/caesar', headers=headers,data=json.dumps(payload))
    print("[DEBUG] Obtained response: %s" % r.text)

def resolvesubstitutionChallenge():
    """
        Solution of substitution challenge
    """
    url = "http://{}:{}/".format(IP, PORT)
    headers = {'Content-Type' : 'application/json'}

    r = requests.get(url + 'challenges/substitution')
    data = r.json()
    print ("[DEBUG] Obtained challenge ciphertext: %s with len %d" % (data['challenge'], len(data['challenge'])))

    solution = solveSubstituition(data['challenge'])

    payload = { 'cookie' : data['cookie'], 'solution' : solution        }
    print("[DEBUG] Submitted solution is:")
    print(json.dumps(payload, indent=4, separators=(',', ': ')))

    r = requests.post(url+'solutions/substitution', headers=headers,data=json.dumps(payload))
    print("[DEBUG] Obtained response: %s" % r.text)

def resolveotpChallenge():
    """
        Solution of otp challenge
    """
    url = "http://{}:{}/".format(IP, PORT)
    headers = {'Content-Type' : 'application/json'}

    r = requests.get(url + 'challenges/otp')
    data = r.json()
    #print ("[DEBUG] Obtained challenge ciphertext: %s with len %d" % (data['challenge'], len(data['challenge'])))

    # TODO: Add a solution here (conversion from hex to ascii will reveal that the result is in a human readable format)
    a = data['challenge'][2:]

    pText = 'Student ID 1000 gets 0 points'

    evilText = 'Student ID 1001 gets 6 points'

    # cTextHex = '0x161d0c56130b17493e2145625800514555596b52140116457942115d2c0b071b' # # 32 Bytes

    cTextHex = a # # 32 Bytes
    cTextStr = bytearray.fromhex(cTextHex).decode() # # outputs a str

    pTextKey = xorString(pText, cTextStr)

    evilCTextStr = xorString(pTextKey, evilText)
    # convert the string to the bytes
    evilCTextHex = evilCTextStr.encode('utf-8')
    # convert the string bytes to the hexadecimal string
    evilCTextHex = evilCTextHex.hex()

    solution = evilCTextHex

    payload = { 'cookie' : data['cookie'], 'solution' : solution}
    print("[DEBUG] Submitted solution is:")
    print(json.dumps(payload, indent=4, separators=(',', ': ')))

    r = requests.post(url+'solutions/otp', headers=headers,data=json.dumps(payload))
    print("[DEBUG] Obtained response: %s" % r.text)

def parseArgs():               
    """ 
        Function for arguments parsing
    """
    aparser = argparse.ArgumentParser(description='Script demonstrates breaking of simple ciphers: Caesar, Substitution cipher, and OTP.', formatter_class = argparse.RawTextHelpFormatter) 
    aparser.add_argument('--port', required=True, metavar='PORT', help='Port of challenge/response server.')
    aparser.add_argument('--ip', required=True, metavar='PORT', help='Port of challenge/response server.')
    aparser.add_argument("--mode", required=True, choices = ['p', 'c', 's', 'o'], help="p => demonstrates hexadecimal encoding challenge.\
                         \nc => demonstrates breaking of the Caesar cipher.\
                         \ns => demonstrates breaking of the Substitution cipher.\
                         \no => demonstrates breaking of the OTP cipher.")
    args = aparser.parse_args()
    
    return args

def userinput():

    args = parseArgs()
    
    global IP
    IP = args.ip

    global PORT
    PORT = args.port

    if PORT != '5000' or IP != '192.168.56.101': 
        print('Only works on Port 5000, 192.168.56.101 and options of -p, c, s, o!')
        return False
    else:
        print('Input Selection passed')
        return args.mode
    
def main():

    status = userinput()
    if (status == False):
        print('Exiting Now!')

    else:
        print(status)
        if status == "o":
            resolveotpChallenge()
        elif status == "p":
            resolvePlainChallenge()
        elif status == "c":
            resolveCaesarChallenge()
        elif status == "s":
            resolvesubstitutionChallenge()



if __name__ == '__main__':
    main()