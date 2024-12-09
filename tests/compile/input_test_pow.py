# Testing pow with positive integers
print("Testing pow with positive integers")
# Expected output: 8 (2^3)
print(pow(2, 3))
# Expected output: 10000 (10^4)
print(pow(10, 4))
# Expected output: 1 (5^0)
print(pow(5, 0))
print("")

# Testing pow with negative integers
print("Testing pow with negative integers")
# Expected output: 0.125 (2^(-3))
print(pow(2, -3))
# Expected output: 1 (1^(-10))
print(pow(1, -10))
# Expected output: 0.0001 (10^(-4))
print(pow(10, -4))
print("")

# Testing pow with floats
print("Testing pow with floats")
# Expected output: 9.261 (2.1^3)
print(pow(2.1, 3))
# Expected output: 0.25 (0.5^2)
print(pow(0.5, 2))
# Expected output: 1 (10.0^0)
print(pow(10.0, 0))
print("")

# Testing pow with a modulus
print("Testing pow with a modulus")
# Expected output: 1 ((3^4) % 5)
print(pow(3, 4, 5))
# Expected output: 0 ((10^3) % 2)
print(pow(10, 3, 2))
# Expected output: 4 ((7^2) % 9)
print(pow(7, 2, 9))
print("")

# Testing pow with base 0 and positive exponent
print("Testing pow with base 0 and positive exponent")
# Expected output: 0 (0^5)
print(pow(0, 5))
# Expected output: 0 (0^3)
print(pow(0, 3))
print("")

# Testing pow with base 0 and exponent 0 (edge case)
print("Testing pow with base 0 and exponent 0")
# Expected output: 1 (0^0, defined as 1 in Python)
print(pow(0, 0))
print("")

# Testing pow with negative base and even/odd exponents
print("Testing pow with negative base and even/odd exponents")
# Expected output: 16 ((-2)^4)
print(pow(-2, 4))
# Expected output: -8 ((-2)^3)
print(pow(-2, 3))
print("")

# Testing pow with very large numbers
print("Testing pow with very large numbers")
# Expected output: A large number (2^100)
print(pow(2, 100))
# Expected output: A large number (3^50)
print(pow(3, 50))
print("")

# Testing pow with modulus and very large numbers
print("Testing pow with modulus and very large numbers")
# Expected output: inf (using modulus to limit result)
print(pow(2, 100000, 1000000007))
# Expected output: -inf (using modulus to limit result)
print(-pow(3, 50000, 1000000007))
print("")
