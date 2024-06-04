import os
import img2pdf

# Replace the directory path with the folder containing JPEG images to be converted
# directory_path = "D:/TKH/4. Course/4_100_Books/GrayHatHacking/"

directory_path = "D:/TKH/4. Course/4_100_Books/AttackingNetworkProtocols/"

# # GrayHatHacking # # completed PDF generation into 3 PDF files
# # AttackingNetworkProtocols

# List all files in the directory and filter only JPEG images (ending with ".gif")
image_files = {
    (os.path.getmtime(directory_path + i)): str(directory_path + i) 
    for i in os.listdir(directory_path) if i.endswith(".gif") 
    } 

# # # sexist way of coding # # # 
sorted_image_files_List = [
    dict(sorted(image_files.items()))[key] for key in dict(sorted(image_files.items())).keys()
]

ten_pages = sorted_image_files_List[:10]

print(ten_pages)

file = open(directory_path + "AttackingNetworkProtocols.pdf", "ab")

# # writing pdf files with byte in longer way
# pdf_bytedata = img2pdf.convert(sorted_image_files_List)
# # # or 
# pdf_bytedata = img2pdf.convert(ten_pages)
# file.write(pdf_bytedata)

dpix = dpiy = 100
layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
# writing pdf files with chunks
# file.write(img2pdf.convert(sorted_image_files_List[1000:], layout_fun=layout_fun))
file.write(img2pdf.convert(sorted_image_files_List, layout_fun=layout_fun))


# closing pdf file
file.close()
print("File is ready")

# # # https://pypi.org/project/img2pdf/
# # use a fixed dpi of 300 instead of reading it from the image
# dpix = dpiy = 300
# layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
# with open("name.pdf","wb") as f:
# 	f.write(img2pdf.convert('test.jpg', layout_fun=layout_fun))

# with open(directory_path + "output.pdf", "a+") as file:
#     for myfilename in (ten_pages):
#         print(myfilename)
#         pdf_bytedata = img2pdf.convert(directory_path + myfilename)
#         file.write(pdf_bytedata)

# file.close()
# pdf_bytedata = img2pdf.convert(Image.open(ten_pages))

# # # Write the PDF content to a file (make sure you have write permissions for the specified file)
# with open(directory_path + "output.pdf", "wb") as file:
#      file.write(pdf_bytedata)

# file.close()


# img2pdf.convert()
# sorted_image_files_Dict = dict(sorted(image_files.items()))
# print((sorted_image_files_Dict)) # # above code returns a <class 'dict'>, {1714631834.1265488: 'page_1.gif', 1714631835.843447: 'page_2.gif', ...

# sorted_image_files_List = sorted(image_files.items())
# print((sorted_image_files_List)) # # above code returns a <class 'list'>, [(1714631834.1265488, 'page_1.gif'), (1714631835.843447, 'page_2.gif'), ...


# # # # safest and long way of coding # # # 
# sorted_image_files_Dict = dict(sorted(image_files.items()))
# sorted_image_files_List = []
# for key in sorted_image_files_Dict.keys():
#     print(sorted_image_files_Dict[key], "->", key)     # # ..., page_1560.gif -> 1714637067.5427516 
#     sorted_image_files_List.append(sorted_image_files_Dict[key])

# print(sorted_image_files_List[:10]) # # ['page_1.gif', 'page_2.gif', ...
# # # # safest and long way of coding # # # 

# # # safer and a bit shorter way of coding # # # 
# sorted_image_files_Dict = dict(sorted(image_files.items()))
# sorted_image_files_List = [
#     sorted_image_files_Dict[key] for key in sorted_image_files_Dict.keys()
# ]
# # # safer and a bit shorter way of coding # # # 

# print(sorted_image_files_List)




# print((image_files(0)))
# print((image_files(1)))
# print((image_files(2)))

# print(image_files.sort())

# print(os.path.getctime(image_files[0]))
# print(os.path.getctime(image_files[1]))
# print(os.path.getctime(image_files[3]))


# image_files2 =[]
# for i in os.listdir(directory_path):
#     if i.endswith(".gif"):
#         image_files2.append([os.path.getmtime(directory_path + i),i]) 

# # sorted_image_files_Dict = image_files.sort(os.path.getctime(image_files))


# # image_files2 =[]
# # for i in os.listdir(directory_path):
# #     if i.endswith(".gif"):
# #         image_files2.append(directory_path + i) 

# print((image_files2[0]))
# print((image_files2[1]))
# print((image_files2[2]))


# print((image_files2[0][0]))
# print((image_files2[1][0]))
# print((image_files2[2][0]))

# # print(os.path.getmtime(image_files[1]))


# # print(image_files.sort(os.path.getmtime))



# # # creating list through list comprehension method
# # my_list = [(str(number) + "hello")  for number in range(1, 10)]

# # # printing newly created list
# # print(my_list)

# # # # ['1hello', '2hello', '3hello', '4hello', '5hello', '6hello', '7hello', '8hello', '9hello']




