print("Testing str with integers")
# '123'
print(str(123))
# '-456'
print(str(-456))
print("")

print("Testing str with floats")
# '3.14'
print(str(3.14))
# '-0.001'
print(str(-0.001))
print("")

print("Testing str with lists")
# '[1, 2, 3]'
print(str([1, 2, 3]))
# "['a', 'b', 'c']"
print(str(['a', 'b', 'c']))
print("")

print("Testing str with tuples")
# '(1, 2, 3)'
print(str((1, 2, 3)))
# "('a', 'b', 'c')"
print(str(('a', 'b', 'c')))
print("")

print("Testing str with dicts")
# '{1: 'One', 2: 'Two', 3: 'Three'}'
print(str({1 : "One", 2 : "Two", 3 : "Three"}))
# "{1: 'One', 2: 'Two', 3: 'Three'}"
print(str({'a' : "ei", 'b' : "bi", 'c' : "ci"}))
print("")

print("Testing str with None and booleans")
# 'None'
print(str(None))
# 'True'
print(str(True))
# 'False'
print(str(False))
print("")

print("Testing empty str")
# ''
print(str())
print("")