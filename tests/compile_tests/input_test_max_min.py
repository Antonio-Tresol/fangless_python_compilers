# Testing max with a list of integers
print("Testing with a list of integers")
print("\nMax")
# Expected output: 10
print(max([1, 5, 10, 3]))
# Expected output: -1
print(max([-10, -5, -1, -3]))
print("\nMin")
# Expected output: 1
print(min([1, 5, 10, 3]))
# Expected output: -10
print(min([-10, -5, -1, -3]))
print("")

# Testing max with a list of strings
print("Testing with a list of strings")
print("\nMax")
# Expected output: 'zebra'
print(max(["apple", "zebra", "mango"]))
# Expected output: 'world'
print(max(["hello", "world", "python"]))
print("\nMin")
# Expected output: 'apple'
print(min(["apple", "zebra", "mango"]))
# Expected output: 'hello'
print(min(["hello", "world", "python"]))
print("")

# Testing max with mixed data types (only comparable types)
print("Testing with a list of floats")
print("\nMax")
# Expected output: 5.5
print(max([1.1, 3.3, 5.5, 2.2]))
print("\nMin")
# Expected output: 1.1
print(min([1.1, 3.3, 5.5, 2.2]))
print("")

# Testing max with individual arguments
print("Testing with individual arguments")
print("\nMax")
# Expected output: 100
print(max(10, 20, 100, 50))
# Expected output: 'world'
print(max("hello", "python", "world"))
print("\nMin")
# Expected output: 10
print(min(10, 20, 100, 50))
# Expected output: 'hello'
print(min("hello", "python", "world"))
print("")