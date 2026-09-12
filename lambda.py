def add(x, y):
    return x + y

sum = add(5, 10)
print(sum)

# 1. name. 2. arguments 3. body

# lambda arguments : body

# add = lambda x, y : x + y

print((lambda x, y : x + y)(10, 5))

# listOfPens.sort(lambda To Sort)

my_add = add
result = my_add(5,10)
print(result)