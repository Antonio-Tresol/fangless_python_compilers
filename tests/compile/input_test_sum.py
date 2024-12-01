# Testing sum with a list of integers
print("Testing sum with a list of integers")
# Expected output: 15
print(sum([1, 2, 3, 4, 5]))
# Expected output: 0
print(sum([]))
# Expected output: -5
print(sum([-5, 0]))
print("")

# Testing sum with a list of floats
print("Testing sum with a list of floats")
# Expected output: 10.5
print(sum([1.5, 2.5, 3.5, 3.0]))
# Expected output: 0.0
print(sum([]))
# Expected output: -7.8
print(sum([-2.5, -5.3]))
print("")

# Testing sum with a tuple of numbers
print("Testing sum with a tuple of numbers")
# Expected output: 6
print(sum((1, 2, 3)))
# Expected output: -10
print(sum((-1, -2, -3, -4)))
# Expected output: 0
print(sum((0,)))
print("")

# # Testing sum with a range
# print("Testing sum with a range")
# # Expected output: 10 (sum of numbers from 1 to 4)
# print(sum(range(1, 5)))
# # Expected output: 0 (empty range)
# print(sum(range(0)))
# # Expected output: -15 (sum of numbers from -5 to -1)
# print(sum(range(-5, 0)))
# print("")

# # Testing sum with an initial value
# print("Testing sum with an initial value")
# # Expected output: 25 (sum of [10, 15] starting from 0)
# print(sum([10, 15], 0))
# # Expected output: 40 (sum of [10, 15] starting from 15)
# print(sum([10, 15], 15))
# # Expected output: -10 (sum of empty list starting from -10)
# print(sum([], -10))
# print("")

# # Testing sum with a set of numbers
# print("Testing sum with a set of numbers")
# # Expected output: 6
# print(sum({1, 2, 3}))
# # Expected output: -6
# print(sum({-1, -2, -3}))
# print("")

# # Testing sum with very large numbers
# print("Testing sum with very large numbers")
# # Expected output: 1000000000
# print(sum([500000000, 500000000]))
# # Expected output: 10000000000
# print(sum([2500000000, 7500000000]))
# print("")

# # Testing sum with floating-point precision
# print("Testing sum with floating-point precision")
# # Expected output: 3.0000000000000004 (due to floating-point precision issues)
# print(sum([1.1, 2.2, -0.3]))
# # Expected output: 0.0
# print(sum([1.1, -1.1]))
# print("")
