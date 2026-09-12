# List / Array

# a = 5
# [10, 20, 30, 40, 50] = Array of Integers -> 5 * 4 bytes = 20 bytes
# What is the type of a? -> Integer -> 4 bytes = 4 * 8 = 32 bits

# int[] arr = {10, 20, 30, 40, 50} | C++/Java
# arr[6] = 60 

# int[] brr = new int[5];

# [][][][][10][20][30][40][50][][][][][][][][][][][][] = RAM
#          arr

# Let's assume [10] is stored at memory location M112
# arr points to M112
# arr[0] = M112 + go to the next address by 0 steps
# arr[1] = M112 + go to the next address by 1 steps

# [[1, 2, 3], [4, 5, 6]] - 2d array
# int[][] arr = new int[3][2]


# List
# A list is nothing but a dynamic array. A dynamic array is an array whose size can change

# list = [] (type int) // initial_size = 5
# new_size=10

# [][][][][][][][][][][][][][][][][][][][][][][10][20][30][50][60][][][][][][][][][][][][] = RAM
#                                               l

# Linked List
# [a|b] = node
# a = data of the node
# b = memory reference of the next node

# my_ll = []
# my_ll.add(10)
# my_ll.add(20)
# my_ll.add(30)
# my_ll.delete(2nd element)

# [30, null][][][10, <address-of-30>][][][][][][][][][][][][][] = RAM
#                       my_ll

# [10][20][30]
# [10]->[20]->[30]->null

# in a LL -> arr[n] = O(n)
# in list -> arr[n] = O(1)

#  For List we use: []
#  For Set we use: {}
#  For Tuple we use: ()
#  For Dict we use: {}


# Set
# A set is like a list but it cannot add duplicates (internal is very different and hard to understand right now)
# my_set = {1, 2, 3}
# my_set.add(1)

# Tuple
# It is extreamly similar to list, but once created, it cannot be changed.

