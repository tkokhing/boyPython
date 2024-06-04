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

# extract and return image files in LIST sorted by date modified 

def returnDirList (directory_path, type_of_file):
    image_files = {
        # os.path.getmtime(directory_path + i): str(directory_path + i) 
        int(i[5:-4]): str(directory_path + i) 
        for i in os.listdir(directory_path) if i.endswith(type_of_file) 
        } 
    # sorted_image_files_List = [
    # dict(sorted(image_files.items()))[key] for key in dict(sorted(image_files.items())).keys()
    # ]
    return [dict(sorted(image_files.items()))[key] for key in dict(sorted(image_files.items())).keys()]


# # # typeoffile = ".gif"
# # # [49:-4]
directory_path = "D:/TKH/4. Course/4_100_Books/AttackingNetworkProtocols/"
length_directory_path = len(directory_path)
print("Directory path length is -->", length_directory_path)
# # # [39:-4]
# directory_path = "D:/TKH/4. Course/4_100_Books/test/"
# type_of_file = ".gif"
# # # GrayHatHacking


# fileNameList = returnDirList(directory_path,".gif")

# print(fileNameList)

# print(len(fileNameList))

# for thisfilename in fileNameList:
#     print(thisfilename)
#     # thisPicture = Image.open(thisfilename)

# print("this is the last gif file",thisfilename)


fileNameList = returnDirList(directory_path,".gif")

# print(fileNameList)

print("The List size is -->",len(fileNameList))

testPicture = Image.open(fileNameList[0])
x_len, y_len = testPicture.size
testPicture.close()

print("picture x_length", x_len)
print("picture y_length", y_len)

for thisfilename in fileNameList:
    print("The file --> ",thisfilename[60:-4])
    thisPicture = Image.open(thisfilename).convert("RGB")
    ImageDraw.Draw(thisPicture).text((x_len - 70, y_len - 30), text = str(thisfilename[60:-4]), fill=(155,0,0), font_size= 20)
    thisPicture.save(thisfilename)
    thisPicture.close()

print("this is the last of the selected gif files",thisfilename)


# thisPicture = Image.open(fileNameList[8])
# # thisPicture.show()

# x_len, y_len = thisPicture.size

# print(x_len)
# print(y_len)

# ImageDraw.Draw(thisPicture).text((x_len - 70, y_len - 30),str(len(fileNameList)-1),fill=(155, 0, 0), font_size= 20)
# thisPicture.save(fileNameList[8])

# thisPicture.show()
# thisPicture.close()

# problem_Pages = []
# page = 1
# endpage = 1561 # # plus 1 to the total page count
# pageloop = 570 # create to loop pages for testing
# page_offset = 1000 # create if need need progressively capture the pages
# filename = 'page_'
# pathDir = 'Advent/'
# while (page != (pageloop + 1) and (page + page_offset != endpage)):

#     # input desire directory
#     thisfilename = pathDir + filename+str(page+page_offset)+'.gif'


#     thisPic = pyautogui.screenshot(thisfilename)

#     # # insert page num and save    
#     ImageDraw.Draw(thisPic).text((x_len - 120, y_len - 50),str(page+page_offset),fill=(155, 0, 0), font_size= 40)
#     thisPic.save(thisfilename)

#     # move to next page
#     pyautogui.hotkey('right')
#     page += 1
#     thisPic.close()
#     # pause a short while so that the page of total page does not pops out
#     tm.sleep(0.5) 
# # returns screen to VScode
# pyautogui.hotkey('alt', 'tab')
# print(problem_Pages)