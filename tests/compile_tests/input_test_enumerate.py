# Testing enumerate with a list
print("Testing enumerate with a list")
# [(0, 'a'), (1, 'b'), (2, 'c')]
print(enumerate(['a', 'b', 'c']))
print("")

# Testing enumerate with a tuple
print("Testing enumerate with a tuple")
# [(0, 10), (1, 20), (2, 30)]
print(enumerate((10, 20, 30)))
print("")

# Testing enumerate with a string
print("Testing enumerate with a string")
# [(0, 'h'), (1, 'e'), (2, 'l'), (3, 'l'), (4, 'o')]
print(enumerate("hello"))
print("")

# Testing enumerate with a set
print("Testing enumerate with a set")
# [(0, 'a'), (1, 'c'), (2, 'b')]
print(enumerate({'a', 'b', 'c'}))
print("")

# Testing enumerate with dictionaries (iterates over keys)
print("Testing enumerate with dictionaries")
# [(0, 'key1'), (1, 'key2')]
print(enumerate({'key1': 100, 'key2': 200}))
print("")

# Testing enumerate with custom starting index
print("Testing enumerate with custom starting index")
# [(5, 'x'), (6, 'y'), (7, 'z')]
print(enumerate(['x', 'y', 'z'], 5))
print("")

# Testing enumerate with range
print("Testing enumerate with range")
# [(0, 1), (1, 2), (2, 3)]
print(enumerate(range(1, 4)))
print("")

# Testing enumerate with an empty iterable
print("Testing enumerate with an empty iterable")
# []
print(enumerate([]))
print("")
