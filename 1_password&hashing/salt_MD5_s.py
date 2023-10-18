# bit size testing adding salt 
 
from typing import Dict, List
import hashlib 
import random
import string
import timeit as tm


class CrackPassword:

    # variables not inside the constructor methods are called 
    # class variables
    # req_file_format =''    

    hashDictStatus = {}

    # what is self? 
    # self represents all Emp_#, => Emp_1.Employee(first, last, pay) 
    # Emp_# are called instance
    # self is called   the     instance

    def __init__(self):
        pass
    
    # for constucting initial hashes List
    def constructHashList():
        hashList =[]
        with open('272727.txt','r') as File1:
            FileContent = File1.readlines()
            for line in FileContent:
                cleanLine = line.replace("\n",'')
                eachHash = cleanLine.split()
                hashList.extend(eachHash)
        return hashList

    # for writing txt file
    def outputFile(fileName, header, message,timeTaken):
        print('Printing text file now')
        saveFile = open(fileName,'w')
        saveFile.write(header)
        messageLength = len(message)
        i = 0 
        while (i != messageLength):
            sentence = str((message[i]) +'\n')
            saveFile.write(sentence)
            i += 1
        saveFile.write(timeTaken)
        saveFile.close()

        
    def addSaltToPassword(hashDictStatus):
        
        pass6List = []
        salted6List = []
        for eachKey in hashDictStatus.keys():
            if hashDictStatus[eachKey][1] == 'Password found':
                print(hashDictStatus[eachKey][0])
                tempWord = (hashDictStatus[eachKey][0]) + random.choice(string.ascii_lowercase)
                pass6List.append(tempWord)
                # pass6Dict[hashlib.md5(tempWord.encode()).hexdigest()] = [tempWord,'Password found']
                salted6List.append(hashlib.md5(tempWord.encode()).hexdigest())
                # hashDictNotFound[eachKey] = hashDictStatus[eachKey]
        
        # print(pass6Dict)
        
        # CrackPassword.outputFile("salted6.txt","", pass6List, "")
        CrackPassword.outputFile("2pass6.txt","", pass6List, "")
        CrackPassword.outputFile("2salted6.txt","", salted6List, "")



def main():

    # charList_alpha = 'abcdef' # tester only
    charList_alpha = 'abcdefghijklmnopqrstuvwxyz'

    # charList_alpha_digit = 'abcdef123' # tester only
    charList_alpha_digit = 'abcdefghijklmnopqrstuvwxyz1234567890'

    # assignment of Class CrackPassword
    hash_to_crack = CrackPassword
    hashList = hash_to_crack.constructHashList()
    # Given all hashes with initial status and ----- as password
    hashDictStatus : Dict[str, List[str]] = { eachHash: ['-----', 'Not found'] for eachHash in hashList}

    print('\nBuild up Hash Dictionary')

    # # testing adding salt function
    hash_to_crack.addSaltToPassword(hashDictStatus)


if __name__ == "__main__":
    main()

 


 