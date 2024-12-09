# Testing round with positive floats (default precision)
print("Testing round with positive floats (default precision)")
# Expected output: 3
print(round(3.14159))
# Expected output: 8
print(round(7.5))
# Expected output: 2
print(round(2.49))
print("")

# Testing round with negative floats (default precision)
print("Testing round with negative floats (default precision)")
# Expected output: -3
print(round(-3.14159))
# Expected output: -8
print(round(-7.5))
# Expected output: -2
print(round(-2.49))
print("")

# Testing round with integers (no effect expected)
print("Testing round with integers")
# Expected output: 5
print(round(5))
# Expected output: -10
print(round(-10))
# Expected output: 0
print(round(0))
print("")

# Testing round with positive floats and specified precision
print("Testing round with positive floats and specified precision")
# Expected output: 3.14 (rounded to 2 decimal places)
print(round(3.14159, 2))
# Expected output: 3.142 (rounded to 3 decimal places)
print(round(3.14159, 3))
# Expected output: 3.0 (rounded to 0 decimal places)
print(round(3.14159, 0))
print("")

# Testing round with zero as input
print("Testing round with zero as input")
# Expected output: 0
print(round(0))
# Expected output: 0.00 (rounded to 2 decimal places)
print(round(0, 2))
# Expected output: 0.0 (rounded to 1 decimal place)
print(round(0, 1))
print("")

# Testing round with large numbers
print("Testing round with large numbers")
# Expected output: 1000000000
print(round(999999999.99999))
# Expected output: 12345678901.230000
print(round(12345678901.23456, 2))
print("")

# Testing round with negative precision (rounding to nearest tens, hundreds, etc.)
print("Testing round with negative precision")
# Expected output: 120 (rounded to nearest 10)
print(round(123, -1))
# Expected output: 100 (rounded to nearest 100)
print(round(123, -2))
# Expected output: 0 (rounded to nearest 1000)
print(round(-123, -3))
print("")

# Testing round with special cases (halfway values)
print("Testing round with special cases (halfway values)")
# Expected output: 5 (rounds to nearest even number)
print(round(4.5))
# Expected output: 6 (rounds to nearest even number)
print(round(5.5))
# Expected output: -4 (rounds to nearest even number)
print(round(-4.5))
print("")
