# Explaining ** in Python

# kwargs is a keyword argument.
# It is used to pass a variable number of keyword arguments to a function.
def test_function(**kwargs):
    # {name: "John", age: 20, city: "New York"}
    print(kwargs)

test_function(name="John", age=20, city="New York")

# **kwargs is a dictionary that contains the key-value pairs of the arguments passed to the function.
# Example:
# test_function(name="John", age=20, city="New York") will be converted to:
# kwargs = {"name": "John", "age": 20, "city": "New York"}
# test_function(**kwargs) will be converted to:
# test_function(name="John", age=20, city="New York")