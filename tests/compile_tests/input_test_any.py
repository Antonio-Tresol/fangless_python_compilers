# Testing any with lists
print("Testing any with lists")
# True
print(any([False, False, True]))
# True
print(any([1, 0, 0]))
# False
print(any([]))
print("")

# Testing any with tuples
print("Testing any with tuples")
# False
print(any((0, 0, 0, 0)))
# True
print(any((0, 1, 0)))
print("")

# Testing any with sets
print("Testing any with sets")
# False
print(any({0, 0, 0}))
# True
print(any({0, 1}))
print("")

# Testing any with strings
print("Testing any with string")
# True
print(any("hello"))
# False
print(any(""))
print("")

# Testing any with dictionaries (checks keys)
print("Testing any with dictionaries")
# False
print(any({}))
# True
print(any({'a': 0, 'b': 1}))
# False
print(any({0: 'zero', 0: 'still zero'}))
print("")

# Testing any with mixed types
print("Testing any with mixed types")
# False
print(any([None, False, '', 0]))
# True
print(any([None, False, 'string', 0]))
# True
print(any([[False], [], [0]]))
# False
print(any([None]))
# False
print(any([False, None, (), [], 0]))
# True
print(any([False, None, (1,), [], 0]))
print("")