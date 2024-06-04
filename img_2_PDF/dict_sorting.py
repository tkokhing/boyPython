# dictionary = {"cat": "chat", "dog": "chien", "horse": "cheval","elephant":"xiang"}

dictionary = {1: "chat", 2: "chien", 4: "cheval",3:"xiang"}

print((dictionary))

# for key in dictionary.keys():
#     print(key, "->", dictionary[key]) 

# print(sorted(dictionary.keys()))

# newDict = sorted(dictionary.keys())

# print(newDict)
# print((dictionary))

print(dict(sorted(dictionary.items())))


newDict2 = dict(sorted(dictionary.items()))

print(newDict2)
# print(newDict2[key])
    
for key in newDict2.keys():
    print(key, "->", newDict2[key]) 
