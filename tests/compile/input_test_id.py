# Testing id with integers
print("Testing id with integers")
# Different memory addresses for different integers
print(id(10))
print(id(20))
# Same memory address for same integer object
print(id(10))
print("")

# Testing id with strings
print("Testing id with strings")
# Different memory addresses for different strings
print(id("hello"))
print(id("world"))
# Same memory address for same string object (strings are immutable)
print(id("hello"))
print("")

# Testing id with lists
print("Testing id with lists")
# Different memory addresses for different lists
a = [1, 2, 3]
b = [4, 5, 6]
print(id(a))
print(id(b))
# Same memory address for the same list object
a_copy = a
print(id(a))
print(id(a_copy))
print("")

# Testing id with tuples
print("Testing id with tuples")
# Different memory addresses for different tuples
print(id((1, 2, 3)))
print(id((4, 5, 6)))
# Same memory address for the same tuple object
t = (1, 2, 3)
t_copy = t
print(id(t))
print(id(t_copy))
print("")

# Testing id with dictionaries
print("Testing id with dictionaries")
# Different memory addresses for different dictionaries
dict1 = {'a': 1, 'b': 2}
dict2 = {'x': 10, 'y': 20}
print(id(dict1))
print(id(dict2))
# Same memory address for the same dictionary object
dict_copy = dict1
print(id(dict1))
print(id(dict_copy))
print("")


# Testing id with None
print("Testing id with None")
# The id of None is always the same
print(id(None))
print(id(None))
print("")
