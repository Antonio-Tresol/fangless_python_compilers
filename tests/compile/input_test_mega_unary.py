print("Numeric Negation:")
print(-42)                   # Expected: -42
print(-(-100))               # Expected: 100 (double negation)
print(-(5 + 10 * 2))         # Expected: -25
print(-3.14)                 # Expected: -3.14
print(-0)                    # Expected: 0 (negation of zero remains zero)
print(-42)                   # Expected: -42
print(-(-999))               # Expected: 999
print(-float('inf'))         # Expected: -inf
print(-float('nan'))         # Expected: nan (negation has no effect on NaN)
print(-(2**31))              # Expected: Large negative number

print("\nLogical Not:")
print(not True)            # Expected: False
print(not False)           # Expected: True
print(not (5 > 10))        # Expected: True
print(not (5 == 5))        # Expected: False
print(not 0)               # Expected: True (0 is considered False)
print(not 42)              # Expected: False (non-zero is True)
print(not [])              # Expected: True (empty list is False)
print(not [1, 2, 3])       # Expected: False (non-empty list is True)
print(not 1)               # Expected: False (non-zero is truthy)
print(not 0)               # Expected: True (zero is falsy)
print(not "string")        # Expected: False (non-empty string is truthy)
print(not "")              # Expected: True (empty string is falsy)
print(not None)            # Expected: True (None is falsy)
print(not [0])             # Expected: False (non-empty list is truthy)
print(not [])              # Expected: True (empty list is falsy)
print(not (5 > 3))         # Expected: False
print(not (10 == 10))      # Expected: False
print(not (5 * 0))         # Expected: True (0 is falsy)
print(not (7 % 2 == 0))    # Expected: True (7 is odd)


print("\nBitwise NOT (~):")
print(~0)                  # Expected: -1
print(~1)                  # Expected: -2
print(~(-5))               # Expected: 4
print(~1024)               # Expected: -1025
print(~(8 | 2))            # Expected: -11 (binary 1010 => NOT => -11)
print(~0)                  # Expected: -1
print(~-1)                 # Expected: 0
print(~255)                # Expected: -256 (complement of 11111111)


print("\nCombinations of Unary Operations:")
print(-(~5))               # Expected: 6 (bitwise NOT and negation)
print(~(-42))              # Expected: 41
print(-(not True))         # Expected: -1 (False is cast to 0, negated to -1)
print(~(not False))        # Expected: -2 (True is cast to 1, ~1 = -2)
print(-~0)                 # Expected: -1 (bitwise NOT of 0 is -1, negated)
print(~-42)                # Expected: 41 (negate first, then bitwise NOT)
print(-(not False))        # Expected: -1 (False becomes True, negated to -1)
print(~(not True))         # Expected: -2 (True becomes 1, bitwise NOT)
print(-sum([1, 2, 3]))     # Expected: -6 (sum is 6, negated)


# print("\nAdvanced Expressions:")
# print(~(5 & 3))            # Expected: -4 (binary 0101 & 0011 = 0001, ~1 = -2)
# print(-(not (8 % 2 == 0))) # Expected: 0 (8 % 2 == 0 is True, not True = False, -False = 0)
# print(-(~(5 << 1)))        # Expected: 10 (shift left 5 to 10, then ~ and negate back)
# print(~len("test"))        # Expected: -5 (length is 4, ~4 = -5)


# print("\nMixing Logical and Bitwise:")
# print(~int(not 0))         # Expected: -2 (not 0 = True, int(True) = 1, ~1 = -2)
# print(-int(not []))        # Expected: -1 (not [] = True, int(True) = 1, negated)
# print(-bool(" "))          # Expected: -1 (non-empty string is True)


# print("\nUnary Operations with Iterables:")
# gen = range(3)
# print(not any(gen))        # Expected: False (non-empty generator is truthy)
# print(-min([10, 20, 5]))   # Expected: -5 (minimum value negated)
# print(~max((1, 2, 3)))     # Expected: -4 (maximum value is 3, ~3 = -4)


# print("\nBitwise NOT with Shifts:")
# print(~(2 << 3))           # Expected: -17 (2 << 3 = 16, ~16 = -17)
# print(~(4 >> 1))           # Expected: -3 (4 >> 1 = 2, ~2 = -3)