# Testing bool with integers
print("Testing bool with integers")
# True
print(bool(1))
# False
print(bool(0))
# True
print(bool(-100))
print("")

# Testing bool with floats
print("Testing bool with floats")
# True
print(bool(3.14))
# False
print(bool(0.0))
# True
print(bool(-0.001))
print("")

# Testing bool with strings
print("Testing bool with strings")
# True
print(bool("hello"))
# False
print(bool(""))
# True
print(bool(" "))
print("")

# Testing bool with lists
print("Testing bool with lists")
# True
print(bool([1, 2, 3]))
# False
print(bool([]))
# True
print(bool([0]))
print("")

# Testing bool with tuples
print("Testing bool with tuples")
# True
print(bool((1, 2)))
# False
print(bool(()))
# True
print(bool((False,)))
print("")

# Testing bool with sets
print("Testing bool with sets")
# True
print(bool({1, 2, 3}))
# False
print(bool(set()))
print("")

# Testing bool with dictionaries
print("Testing bool with dictionaries")
# True
print(bool({"key": "value"}))
# False
print(bool({}))
print("")

# Testing bool with None
print("Testing bool with None")
# False
print(bool(None))
print("")