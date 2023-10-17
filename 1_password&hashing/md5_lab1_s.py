# 10***92, tkokhing

from typing import Dict, List
import argparse
import hashlib 
import random
import string
import timeit as tm


class CrackPassword:

    # Class variables for inheritance 
    hashDictStatus = {}
    INPUT_FILE = ''
    DICT_FILE = ''
    OUTPUT_FILE = ''

    # for constucting initial hashes List
    def constructHashList(INPUT_FILE):
        hashList =[]
        with open(INPUT_FILE,'r') as File1:
            FileContent = File1.readlines()
            for line in FileContent:
                cleanLine = line.replace("\n",'')
                eachHash = cleanLine.split()
                hashList.extend(eachHash)
        return hashList

    # for writing txt file
    def outputFile(fileName, header, message,timeTaken, fileState):
        print('Printing text file now')
        saveFile = open(fileName, fileState)
        saveFile.write(header)
        messageLength = len(message)
        i = 0 
        while (i != messageLength):
            sentence = str((message[i]) +'\n')
            saveFile.write(sentence)
            i += 1
        saveFile.write(timeTaken)
        print('\n')
        saveFile.close()

    # For dictAttack, passing Dict of hashes with its status
    def dictAttack(hashDictStatus, DICT_FILE, OUTPUT_FILE):
        start = tm.default_timer()
        messageToWrite = []
        fileMessage = 'Words found using provided Dictionary \n'
        foundHashCounter = 0

        hashDictLength = len(hashDictStatus)    

        with open(DICT_FILE,'r') as word5clue:

            FileContent = word5clue.readlines()
            for line in FileContent:
                cleanLine = line.replace("\n",'') # must clean the line
                hashed = hashlib.md5(cleanLine.encode()).hexdigest()

                for eachHash in hashDictStatus:
                    # print(eachHash)
                    if eachHash == hashed:
                        # print('Hash: ', hashed,' -> password: ', cleanLine)
                        foundWord = 'Hash: ' + hashed + ' -> password: ' + cleanLine
                        messageToWrite.append(foundWord)
                        foundHashCounter += 1
                        hashDictStatus[eachHash] = [cleanLine,'Password found']
                    
                    # jump out once all hashes are cracked
                    if hashDictLength == foundHashCounter:
                        break

        end = tm.default_timer()

        timeTaken = 'Time taken is: ' + str(end - start) + ' for [' +str(foundHashCounter) + '] out of ' + str(hashDictLength) + ' found.'
        
        
        print('Inside dictAttack', DICT_FILE, OUTPUT_FILE)

        CrackPassword.outputFile(OUTPUT_FILE,fileMessage, messageToWrite, timeTaken,'w')    


    # For BruteForce, passing charList of either alphabets only or alphanumeric and 
    # passing Dict of hashes with its status which is used to, example 
    # {'f6cc7e9c3fa3afa73888d3705c266715': ['cbsanw', 'Password found'], \
    #  '669141e1b9639f5e793aaab1e69da0c4': ['-----', 'Not found'], \
    #  '21d058fb362e97466ef76233fca14fa1': ['omtoao', 'Password found'], ...

    # Status used for filtering out those hashes that have been cracked
    # making processing time shorter for only those that have yet to crack 

    def bruteForce(charList, hashDictStatus, OUTPUT_FILE):
        start = tm.default_timer()
        hashDictNotFound ={}
        messageToWrite = []
        foundHashCounter = 0
        hashDictNotFoundLength = 0
        len_charList = len(charList)
        
        if len_charList == 26:
            fileMessage = '\nNew Words found using Bruteforce with lowercase \n'

        else:
            fileMessage = '\nNew Words found using Bruteforce with lowercase and digits \n'
        
        hashDictLength = len(hashDictStatus)    

        # Creates another temp Dict for those hashed with 'Not Found' status 
        for eachKey in hashDictStatus.keys():
            if hashDictStatus[eachKey][1] == 'Not found':
                hashDictNotFound[eachKey] = hashDictStatus[eachKey]
                hashDictNotFoundLength += 1

        for i in range (0,len_charList):
            for j in range (0,len_charList):
                for k in range (0,len_charList):
                    for l in range (0,len_charList):
                        for m in range (0,len_charList):
                            tempWord = str(charList[i]) + str(charList[j]) + str(charList[k]) + str(charList[l]) + str(charList[m])
                            hashed = hashlib.md5(tempWord.encode()).hexdigest()

                            for eachHash in hashDictNotFound:
                                # print(eachHash)
                                if eachHash == hashed:
                                    print('Hash: ', hashed,' +++++++++++++++-> password: ', tempWord)
                                    foundWord = 'Hash: ' + hashed + ' -> password: ' + tempWord
                                    messageToWrite.append(foundWord)
                                    foundHashCounter += 1
                                    hashDictStatus[eachHash] = [tempWord,'Password found']
                            
                            # jump out once all hashes are cracked
                            if hashDictNotFoundLength == foundHashCounter:
                                break

        end = tm.default_timer()

        timeTaken = 'Time taken is: ' + str(end - start) + ' for [' +str(foundHashCounter) + '] out of ' + str(hashDictLength) + ' found.'
        
        CrackPassword.outputFile(OUTPUT_FILE,fileMessage, messageToWrite, timeTaken, 'a')    

    def addSaltToPassword(hashDictStatus):
        
        pass6List = []
        salted6List = []
        for eachKey in hashDictStatus.keys():
            if hashDictStatus[eachKey][1] == 'Password found':
                tempWord = (hashDictStatus[eachKey][0]) + random.choice(string.ascii_lowercase)
                pass6List.append(tempWord)
                salted6List.append(hashlib.md5(tempWord.encode()).hexdigest())

        CrackPassword.outputFile("pass6.txt","", pass6List, "", 'w')
        CrackPassword.outputFile("salted6.txt","", salted6List, "",'w')

def parseArgs():               

    aparser = argparse.ArgumentParser(description='For cracking paswords using Dictionary, Bruteforce, Hashcat.', formatter_class = argparse.RawTextHelpFormatter) 
    aparser.add_argument('-i', '-inputfile', type = str, required=True, metavar='', help='Enter name for input file.')
    aparser.add_argument('-w', '-writefile', type = str, required=True, metavar='', help='Enter name for dictionary file.')
    aparser.add_argument('-o', '-outputfile', type = str, required=True, metavar='', help='Enter name for output file.')
    args = aparser.parse_args()
    
    return args

def main():

    args = parseArgs()
  
    # charList_alpha = 'abcdef' # tester only
    charList_alpha = 'abcdefghijklmnopqrstuvwxyz'

    # charList_alpha_digit = 'abcdef123' # tester only
    charList_alpha_digit = 'abcdefghijklmnopqrstuvwxyz1234567890'

    # assignment of Class CrackPassword
    hash_to_crack = CrackPassword

    INPUT_FILE = args.i
    DICT_FILE = args.w
    OUTPUT_FILE = args.o
    
    hashList = hash_to_crack.constructHashList(INPUT_FILE)
    
    # Given all hashes with initial status and ----- as password
    hashDictStatus : Dict[str, List[str]] = { eachHash: ['-----', 'Not found'] for eachHash in hashList}

    thissessionLogIn = True
    
    while (thissessionLogIn):
        print('\n')
        print('===================================================','\n')
        print('\t','[1] - Dictionary Attack')
        print('\t','[2] - Bruteforce with only lowercase')
        print('\t','[3] - Bruteforce with only lowercase and digits')
        print('\t','[4] - Add Salt and make New password')
        print('\t','[0] - Exit','\n')
        sessionInput=input('Please choose? (Enter a number) ')

        if sessionInput == '1':
            print('File [%s] will be GENERATED, please wait' % OUTPUT_FILE)
            hash_to_crack.dictAttack(hashDictStatus, DICT_FILE, OUTPUT_FILE)
            print('\nHash Dictionary after DictAttack')
            print(hashDictStatus)

        elif sessionInput == '2':
            print('File [%s] will be APPENDED, please wait' % OUTPUT_FILE)
            hash_to_crack.bruteForce(charList_alpha,hashDictStatus, OUTPUT_FILE)
            print('\nHash Dictionary after BruteForce')
            print(hashDictStatus)
        
        elif sessionInput == '3':
            print('File [%s] will be APPENDED, please wait' % OUTPUT_FILE)
            hash_to_crack.bruteForce(charList_alpha_digit,hashDictStatus, OUTPUT_FILE)
            print('\nHash Dictionary after BruteForce with Digits')
            print(hashDictStatus)

        elif sessionInput == '4':
            print('You have enter 4')
            print('Files [pass6.txt] and [salted6.txt] will be generated')
            hash_to_crack.addSaltToPassword(hashDictStatus)

        elif sessionInput == '0':
            print('You have enter 0')
            thissessionLogIn = False
 
        else:
            print('Please enter a correct option')

    print('Thank you SUTD for the opportunity')
    input()


if __name__ == "__main__":
    main()
 