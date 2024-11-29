# Testing range with only a stop argument
print("Testing range with only a stop argument")
# Expected output: [0, 1, 2, 3, 4]
print(list(range(5)))
# Expected output: [0]
print(list(range(1)))
# Expected output: [] (empty list)
print(list(range(0)))
print("")

# Testing range with start and stop arguments
print("Testing range with start and stop arguments")
# Expected output: [1, 2, 3, 4]
print(list(range(1, 5)))
# Expected output: [-3, -2, -1, 0, 1, 2]
print(list(range(-3, 3)))
# Expected output: [10, 11, 12, 13]
print(list(range(10, 14)))
print("")

# Testing range with start, stop, and step arguments
print("Testing range with start, stop, and step arguments")
# Expected output: [0, 2, 4, 6, 8]
print(list(range(0, 10, 2)))
# Expected output: [5, 3, 1, -1, -3]
print(list(range(5, -5, -2)))
# Expected output: [100, 120, 140, 160]
print(list(range(100, 180, 20)))
print("")

# Testing range with negative steps
print("Testing range with negative steps")
# Expected output: [10, 9, 8, 7, 6]
print(list(range(10, 5, -1)))
# Expected output: [0, -1, -2, -3, -4]
print(list(range(0, -5, -1)))
# Expected output: [20, 15, 10, 5, 0]
print(list(range(20, -1, -5)))
print("")

# Testing range with large numbers
print("Testing range with large numbers")
# Expected output: A long list from 0 to 9999
a = range(10000)
print(list(a[:10])) 
# Expected output: A long list from 500000 to 500099
print(list(range(500000, 500100)))
print("")

# Testing range with invalid inputs (expecting ValueError or empty list)
print("Testing range with invalid inputs")
# Expected output: [] (empty list)
print(list(range(5, 5)))
# Expected output: [] (empty list)
print(list(range(5, 5, -1)))
# Expected output: [] (empty list)
print(list(range(10, 0, 1)))
print("")