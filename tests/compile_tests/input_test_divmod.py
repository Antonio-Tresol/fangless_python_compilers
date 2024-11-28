# Testing divmod with positive integers
print("Testing divmod with positive integers")
# (3, 1)
print(divmod(10, 3))
# (5, 0)
print(divmod(20, 4))
# (1, 0)
print(divmod(5, 5))
print("")

# Testing divmod with negative integers
print("Testing divmod with negative integers")
# (-3, -1)
print(divmod(-10, 3))
# (-3, 1)
print(divmod(10, -3))
# (3, 1)
print(divmod(-10, -3))
print("")

# Testing divmod with mixed signs
print("Testing divmod with mixed signs")
# (-3, 2)
print(divmod(14, -4))
# (-5, -2)
print(divmod(-17, 3))
# (0, -2)
print(divmod(-2, 7))
print("")

# Testing divmod with zero divisor (expecting an error)
# print("Testing divmod with zero divisor (expecting exception)")
# print(divmod(10, 0))
# print("")

# Testing divmod with floats
print("Testing divmod with floats")
# (2.0, 1.5)
print(divmod(7.5, 3.0))
# (-4.0, -0.5)
print(divmod(-10.5, 2.5))
# (0.0, 5.50)
print(divmod(5.5, 10.0))
print("")

# Testing divmod with mixed float and int
print("Testing divmod with mixed float and int")
# (2.0, 1.5)
print(divmod(7.5, 3))
# (-5.0, -0.5)
print(divmod(-10.5, 2))
# (3.0, 0.75)
print(divmod(12.75, 4))
print("")
