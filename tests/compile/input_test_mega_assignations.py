print("\nSimple Assignments:")
x = 10
y = 5
x += y
# Expected: 15
print("x += y: " + x)
x -= y  # Expected: 10
print("x -= y: " + x)
x *= y  # Expected: 50
print("x *= y: " + x)
x /= y  # Expected: 10.0
print("x /= y: " + x)
x //= y  # Expected: 2.0
print("x //= y: " + x)
x %= y  # Expected: 2.0
print("x %= y: " + x)
x **= y  # Expected: 32.0
print("x **= y: " + x)

print("\nBitwise Assignments:")
a = 5  # 101 in binary
a &= 3  # Expected: 1 (101 & 011 = 001)
print("a &= 3: " + a)
a |= 4  # Expected: 5 (001 | 100 = 101)
print("a |= 4: " + a)
a ^= 7  # Expected: 2 (101 ^ 111 = 010)
print("a ^= 7: " + a)
a <<= 2  # Expected: 8 (010 << 2 = 1000)
print("a <<= 2: " + a)
a >>= 1  # Expected: 4 (1000 >> 1 = 0100)
print("a >>= 1: " + a)

print("\nComplex Assignments with Mixed Operations:")
b = 4
c = 2
d = 3
b += c * d  # Expected: 4 + 6 = 10
print("b += c * d: " + b)
b -= (c + d) ** 2  # Expected: 10 - 25 = -15
print("b -= (c + d) ** 2: " + b)
b *= c << d  # Expected: -15 * 16 = -240
print("b *= c << d: " + b)
b //= (c ^ d)  # Expected: -240 // 1 = -240
print("b //= (c ^ d): " + b)
b %= (d & 1)  # Expected: -240 % 1 = 0
print("b %= (d & 1): " + b)
b **= 3  # Expected: 0 ** 3 = 0
print("b **= 3: " + b)

print("\nAssignments with List and String Operations:")
lst = [1, 2, 3]
lst += [4, 5]  # Expected: [1, 2, 3, 4, 5]
print("lst += [4, 5]: " + lst)
lst *= 2  # Expected: [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
print("lst *= 2: " + lst)
lst[0] = 10  # Expected: [10, 2, 3, 4, 5, 1, 2, 3, 4, 5]
print("lst[0] = 10: " + lst)
str1 = "Hello"
str1 *= 3  # Expected: "HelloHelloHello"
print("str1 *= 3: " + str1)
str1 += " World"  # Expected: "HelloHelloHello World"
print("str1 += ' World': " + str1)
