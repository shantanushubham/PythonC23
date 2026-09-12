# Map<Object, Object> - Java
# unordered_map<object, object> - C++
# {} / Map() - JS


my_dict = {1: "Akash", 2: "Akash", 3: "Abhishek", 1: "Shantanu"}
my_dict[4] = "Ananya"
print(my_dict)
print(my_dict.get(1))
del my_dict[2]

# list(1,2,3) - M1
# list() - M6

# [][M1][][][][] - source
# [][M6][][][][] - target

my_name = [1, 2, 4] # list

my_tuple = (my_name, ) # a tuple that contains a list -> ([])
print(my_tuple)  # ([1,2,3])

my_name.append(10)
print(my_name)
print(my_tuple)  # ([1,2,3,10]
#                       m1
# [][][m1][][][][][][][[1,2,4, 10]][]
#                       mn
