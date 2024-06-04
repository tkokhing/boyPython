# # """
# # Use case: 
# # To insert page number to existing image files
# # """
# # import os
# # # import img2pdf

# # # import pyautogui
# # # import time as tm
# # from PIL import Image, ImageDraw
# # # import numpy as np

# # # extract and return specified filetype in LIST 
# # #   either sorted by date modified 
# # #   or sorted by sequenced filename

# # def return_dir_list (directory_path, type_of_file):
# #     image_files = {
# #         # os.path.getmtime(directory_path + i): str(directory_path + i) 
# #         int(i[5:-4]): str(directory_path + i) 
# #         for i in os.listdir(directory_path) if i.endswith(type_of_file) 
# #         } 
# #     return [dict(sorted(image_files.items()))[key] for key in dict(sorted(image_files.items())).keys()]

# # def testPageSize(testImageFile):
# #     testPicture = Image.open(testImageFile)
# #     x_len, y_len = testPicture.size
# #     testPicture.close() # # always close image
# #     return x_len, y_len

# # def insert_page_number(fileNameList, x_len, y_len):
# #     for thisPathFilename in fileNameList:
# #         print("The file --> ",thisPathFilename[60:-4])
# #         thisPicture = Image.open(thisPathFilename).convert("RGB")
# #         ImageDraw.Draw(thisPicture).text((x_len - 70, y_len - 30), text = str(thisPathFilename[60:-4]), fill=(155,0,0), font_size= 20)
# #         thisPicture.save(thisPathFilename)
# #         thisPicture.close()

# #     print("this is the last of the selected gif files",thisPathFilename)

# # def resizeImage(fileNameList, x_len, y_len):
# #     for thisPathFilename in fileNameList[3:5]:
# #         print("The file --> ",thisPathFilename[39:-4])
# #         thisPicture = Image.open(thisPathFilename)
# #         # thisPicture = thisPicture.resize((round(thisPicture.size[0]*0.5), round(thisPicture.size[1]*0.5)))
# #         thisPicture = thisPicture.resize((round(x_len*0.5), round(y_len*0.5)))
# #         thisPicture.save(thisPathFilename)
# #         thisPicture.close()

# # # # # [49:-4]
# # # directory_path = "D:/TKH/4. Course/4_100_Books/AttackingNetworkProtocols/"

# # # # # [39:-4]
# # directory_path = "D:/TKH/4. Course/4_100_Books/test/"
# # length_directory_path = len(directory_path)
# # print("Directory path length is -->", length_directory_path)

# # fileNameList = return_dir_list(directory_path,".gif")

# # # to extract picture size if, and only if, 
# # # all pictures are known to be of the same size faster this way
# # # else, test page size after Image.open 
# # x_len, y_len = testPageSize(fileNameList[0])

# # # insert_page_number(fileNameList, x_len, y_len)

# .# resizeImage(fileNameList, x_len, y_len)

# extract and return specified filetype in LIST 
#   either sorted by date modified 
#   or sorted by sequenced filename

'''
It starts here
'''

import os
import pyautogui
import time as tm
from PIL import Image, ImageDraw

def insert_page_number(fileNameList, x_len, y_len,directory_path, default_filename='page_', type_of_file='.gif'):
    '''
    create as a method by itself
    For opening a LIST of a existing image files to append page number
    '''
    length_directory_path = len(directory_path+default_filename)
    length_fileExt = len(type_of_file)

    image_font_size = round(y_len/50)
    x_len_offset = image_font_size*3
    y_len_offset = image_font_size*2
    
    for thisPathFilename in fileNameList:
        # print("The filename --> ",thisPathFilename[60:-4])
        thisPicture = Image.open(thisPathFilename).convert("RGB")
        ImageDraw.Draw(thisPicture).text((x_len - x_len_offset, y_len - y_len_offset), text = str(thisPathFilename[length_directory_path:-length_fileExt]), fill=(155,0,0), font_size= image_font_size)
        thisPicture.save(thisPathFilename)
        thisPicture.close()

def capture_image(x_len, y_len, directory_path, default_filename='page_', type_of_file='.gif'):
    '''
    Capture and advance the page screen. 
    Save images in sequential number in default gif format, or
    otherwise specify
    if images are ready, skip this
    '''
    # input desire directory
    page = 1
    endpage = 835 # # plus 1 to the total page count
    pageloop = 835 # create to loop pages for testing, otherwise is = endpage
    page_offset = 0 # create if need need progressively capture the pages

    length_directory_path = len(directory_path+default_filename)
    length_fileExt = len(type_of_file)
    # variables for sizing and positioning page number depending on image size
    # image_font_size = round(y_len/50)
    # x_len_offset = image_font_size*3
    # y_len_offset = image_font_size*2

    while (page != (pageloop + 1) and (page + page_offset != endpage)): 
        # # create sequential filename 
        thisPathFilename = directory_path + default_filename+str(page+page_offset)+type_of_file
        # screenshot and insert page number
        # thisPicture = pyautogui.screenshot(thisPathFilename).convert("RGB")
        # ImageDraw.Draw(thisPicture).text((x_len - x_len_offset, y_len - y_len_offset), text = str(thisPathFilename[length_directory_path:-length_fileExt]), fill=(155,0,0), font_size= image_font_size)
        # thisPicture.save(thisPathFilename)
        # thisPicture.close()
        # print(thisPathFilename)

        # move to next page
        pyautogui.hotkey('right')
        page += 1
        # pause a short while should pages refresh takes time
        tm.sleep(0.5) 

def return_dir_list (directory_path, default_filename='page_', type_of_file='.gif'): 
    '''
    take in a dir path, default filename (or otherwise specify) and returns a LIST of files of a particular file type
    '''
    length_def_filename = len(default_filename)
    length_fileExt = len(type_of_file)
    image_files = {
        # os.path.getmtime(directory_path + i): str(directory_path + i) 
        int(i[length_def_filename:-length_fileExt]): str(directory_path + i) 
        for i in os.listdir(directory_path) if i.endswith(type_of_file) 
        } 
    return [dict(sorted(image_files.items()))[key] for key in dict(sorted(image_files.items())).keys()]

def main():
    """
    Capture the images and compile into a searchable PDF file
    """
    print("Hello World")
    directory_path = "D:/TKH/4. Course/4_100_Books/test/" # or the below
    # directory_path = "D:/TKH/4. Course/4_100_Books/PythonForGeeks/" # or the above
    default_filename = 'page_'
    # to extract picture size if, and only if, 
    # all pictures are known to be of the same size faster this way
    # else, test page size after Image.open 
    pyautogui.hotkey('alt', 'tab')
    x_len, y_len = pyautogui.size()
    print("Screen size is  -->", x_len, y_len)
    pyautogui.moveTo(x_len-1, y_len//2)
    # capture_image(x_len, y_len, directory_path, default_filename,".gif")
    

    fileNameList = return_dir_list(directory_path, default_filename, type_of_file='.gif')
    insert_page_number(fileNameList, x_len, y_len, directory_path, default_filename, type_of_file='.gif')
    print(fileNameList[-4:-1])
    print(main.__doc__)


# def insert_page_number(fileNameList, x_len, y_len,directory_path, default_filename='page_', type_of_file='.gif'):


if __name__ == "__main__":
    main()