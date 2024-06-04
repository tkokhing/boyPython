"""
Use case: 
Say if you have online slides that you prefer to have it offline
 and the means to edit on it. Snap the slides, and turn it into PDF 
 for offline use

Coded with VSCode, on my XPS13  
"""

import pyautogui
import time as tm
from PIL import Image, ImageDraw
import numpy as np

# use mean squared error to compute how alike 2 pictures are 
def mse(imageA, imageB):
    return np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)/float(imageA.size)

def checkPageStatus(thisfilename, width, height):
    try:
        # # determines if the bottom page numbering bar has appeared which is what we do not want
        pyautogui.locateOnScreen('Advent/reference_page.png', region=(0, int(height * 0.89), int(width * 0.05), height), confidence = 0.8)
        # pyautogui.locateOnScreen('Advent/spinning.png', region=(width//2 - 100, height//2 - 200, width//2 + 100, height//2 + 100), confidence = 0.4)
        return True
    except:
        # # print("Exception triggered. Image is not detected")
        return False

# obtain loading page pixels value as baseline, need to redo for diff PC and resolution 
# # # for XPS13
np_loading = np.array(Image.open('D:/TKH/1_Project/1_1_Python/Advent/loading_XPS.gif'))

# # # for UH-X
# np.array(Image.open('D:/kht/1_Project/1_1_Python/Advent/loading.gif'))

# get screen size, toggle to website, move mouse away, to start capturing 
x_len, y_len = pyautogui.size()
pyautogui.hotkey('alt', 'tab')
pyautogui.moveTo(x_len-1, y_len//2)

problem_Pages = []
page = 1
endpage = 1561 # # plus 1 to the total page count
pageloop = 570 # create to loop pages for testing
page_offset = 1000 # create if need need progressively capture the pages
default_filename = 'page_'
pathDir = 'Advent/'
while (page != (pageloop + 1) and (page + page_offset != endpage)):

    # input desire directory
    thisfilename = pathDir + default_filename+str(page+page_offset)+'.gif'

    thisPic = pyautogui.screenshot(thisfilename)

    # testing if spinning at the loading page
    # re-opening file coz screenshot image is 3D (3200, 1800, 3) cannot compare with 2D image
    while (mse(np.array(Image.open(thisfilename)),np_loading) < 9):
        # capture pages that are awaiting loading
        problem_Pages.append(thisfilename[len(pathDir):]) # # take away the directory
        tm.sleep(1)
        # wait awhile and recapture the screen
        thisPic = pyautogui.screenshot(thisfilename)    

    while (checkPageStatus(thisfilename,x_len, y_len)):
        print("inside while loop, still waiting for page to fully load")
        problem_Pages.append(thisfilename[len(pathDir):]) # # take away the directory
        tm.sleep(1)     

    # # insert page num and save    
    ImageDraw.Draw(thisPic).text((x_len - 120, y_len - 50),str(page+page_offset),fill=(155, 0, 0), font_size= 40)
    thisPic.save(thisfilename)

    # move to next page
    pyautogui.hotkey('right')
    page += 1
    thisPic.close()
    # pause a short while so that the page of total page does not pops out
    tm.sleep(0.5) 
# returns screen to VScode
pyautogui.hotkey('alt', 'tab')
print(problem_Pages)