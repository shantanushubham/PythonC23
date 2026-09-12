# In OOP - we have classes and objects

"""
1. Cook the spices
2. Marinate the protiem 
3. Put everything with rice in a pressure cooker
4. Let it cook
"""

# The Idea is Class
# The output from that idea is Object

class Biryani:
    # protienType: string
    # noOfPlates: int
    # spicyOrNonSpicy: boolean

    # Note: Whatever we write inside the class is called a member of the class

    # Constructor
    def __init__(self, protien_type, is_spicy, no_of_plates=1):
        self.protien_type = protien_type
        self.no_of_plates = no_of_plates
        self.is_spicy = is_spicy



# my_biryani = Biryani("Chicken", 1, True)
my_biryani = Biryani()
print(my_biryani)