import os
import img2pdf

# Replace the directory path with the folder containing JPEG images to be converted
directory_path = "D:/TKH/4. Course/4_100_Books/GrayHatHacking/"

# List all files in the directory and filter only JPEG images (ending with ".gif")
image_files = {
    (os.path.getmtime(directory_path + i)): i 
    for i in os.listdir(directory_path) if i.endswith(".gif") 
    } 

# # # sexist way of coding # # # 
sorted_image_files_List = [
    dict(sorted(image_files.items()))[key] for key in dict(sorted(image_files.items())).keys()
]


# # # # safest and long way of coding # # # 
# sorted_image_files_Dict = dict(sorted(image_files.items()))
# sorted_image_files_List = []
# for key in sorted_image_files_Dict.keys():
#     # print(sorted_image_files_Dict[key], "->", key) 
#     sorted_image_files_List.append(sorted_image_files_Dict[key])
# # # # safest and long way of coding # # # 

# # # safer and a bit shorter way of coding # # # 
# sorted_image_files_List = [
#     sorted_image_files_Dict[key] for key in sorted_image_files_Dict.keys()
# ]
# # # safer and a bit shorter way of coding # # # 

print(sorted_image_files_List)




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

# # # Convert the list of JPEG images to a single PDF file
# # pdf_bytedata = img2pdf.convert(image_files)

# # # Write the PDF content to a file (make sure you have write permissions for the specified file)
# # with open("output.pdf", "wb") as file:
# #     file.write(pdf_bytedata)


# # # creating list through list comprehension method
# # my_list = [(str(number) + "hello")  for number in range(1, 10)]

# # # printing newly created list
# # print(my_list)

# # # # ['1hello', '2hello', '3hello', '4hello', '5hello', '6hello', '7hello', '8hello', '9hello']




