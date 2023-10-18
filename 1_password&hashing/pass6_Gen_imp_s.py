# Filename: chk_MD5_length.py
from typing import Dict, List
import hashlib 
import pandas as pd

# hashed = hashlib.md5(line.encode()).hexdigest()

def genSalted6():

    salted6List = []
    with open('D:/kht/10_MSSD/10.5_T3/STL1/Lab1_stl1_Hashes_Passwords/pass6.txt','r') as word6clue:
        FileContent = word6clue.readlines()
        for line in FileContent:
            cleanLine = line.replace("\n",'') # must clean the line
            hashed = hashlib.md5(cleanLine.encode()).hexdigest()
            salted6List.append(hashed)

    # original
    # outputFile("salted6.txt","", salted6List, "")
    
    outputFile("salted6_improved.csv", salted6List)


def outputFile(fileName,message):
    print('Printing text file now')
    df = pd.DataFrame(message)
    df.columns = ['Hashed'] 
    df.to_csv(fileName)   
    
# Customizable 
# def outputFile(fileName, header, message,timeTaken):
#     print('Printing text file now')
#     saveFile = open(fileName,'w')
#     saveFile.write(header)
#     messageLength = len(message)
#     i = 0 
#     while (i != messageLength):
#         sentence = str((message[i]) +'\n')
#         saveFile.write(sentence)
#         i += 1
#     saveFile.write(timeTaken)
#     saveFile.close()

genSalted6()
