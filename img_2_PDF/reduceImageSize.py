"""
Use case: 
To insert page number to existing image files
"""
import os
# import img2pdf

# import pyautogui
# import time as tm
from PIL import Image, ImageDraw
# import numpy as np

# extract and return specified filetype in LIST 
#   either sorted by date modified 
#   or sorted by sequenced filename

def returnDirList (directory_path, type_of_file):
    image_files = {
        # os.path.getmtime(directory_path + i): str(directory_path + i) 
        int(i[5:-4]): str(directory_path + i) 
        for i in os.listdir(directory_path) if i.endswith(type_of_file) 
        } 
    return [dict(sorted(image_files.items()))[key] for key in dict(sorted(image_files.items())).keys()]

def testPageSize(testImageFile):
    testPicture = Image.open(testImageFile)
    x_len, y_len = testPicture.size
    testPicture.close() # # always close image
    return x_len, y_len 

def insertPageNumber(fileNameList, x_len, y_len):
    for thisfilename in fileNameList:
        print("The file --> ",thisfilename[60:-4])
        thisPicture = Image.open(thisfilename).convert("RGB")
        ImageDraw.Draw(thisPicture).text((x_len - 70, y_len - 30), text = str(thisfilename[60:-4]), fill=(155,0,0), font_size= 20)
        thisPicture.save(thisfilename)
        thisPicture.close()

    print("this is the last of the selected gif files",thisfilename)

def resizeImage(fileNameList, x_len, y_len):
    for thisfilename in fileNameList:
        print("The file --> ",thisfilename[39:-4])
        thisPicture = Image.open(thisfilename)
        # thisPicture = thisPicture.resize((round(thisPicture.size[0]*0.5), round(thisPicture.size[1]*0.5)))
        thisPicture = thisPicture.resize((round(x_len*0.5), round(y_len*0.5)))
        thisPicture.save(thisfilename)
        thisPicture.close()

# # # [49:-4]
directory_path = "D:/TKH/4. Course/4_100_Books/AttackingNetworkProtocols/"

# # # [39:-4]
# directory_path = "D:/TKH/4. Course/4_100_Books/test/"
length_directory_path = len(directory_path)
print("Directory path length is -->", length_directory_path)

fileNameList = returnDirList(directory_path,".gif")

# to extract picture size if, and only if, 
# all pictures are known to be of the same size faster this way
# else, test page size after Image.open 
x_len, y_len = testPageSize(fileNameList[0])

# insertPageNumber(fileNameList, x_len, y_len)

resizeImage(fileNameList, x_len, y_len)
