def divide_two_numbers(a, b):
    try:
        return a / b
    except:
        print("Cannot Divide By Zero")

result = divide_two_numbers(10, 0)
print(result)

"""
try:
    <doubtful-code>
except:
    <how to handle the exception>
"""