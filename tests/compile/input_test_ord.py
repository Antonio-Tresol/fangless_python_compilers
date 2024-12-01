# Testing ord with lowercase letters
print("Testing ord with lowercase letters")
# Expected output: 97 (ASCII value of 'a')
print(ord('a'))
# Expected output: 122 (ASCII value of 'z')
print(ord('z'))
# Expected output: 109 (ASCII value of 'm')
print(ord('m'))
print("")

# Testing ord with uppercase letters
print("Testing ord with uppercase letters")
# Expected output: 65 (ASCII value of 'A')
print(ord('A'))
# Expected output: 90 (ASCII value of 'Z')
print(ord('Z'))
# Expected output: 77 (ASCII value of 'M')
print(ord('M'))
print("")

# Testing ord with digits
print("Testing ord with digits")
# Expected output: 48 (ASCII value of '0')
print(ord('0'))
# Expected output: 57 (ASCII value of '9')
print(ord('9'))
# Expected output: 53 (ASCII value of '5')
print(ord('5'))
print("")

# Testing ord with special characters
print("Testing ord with special characters")
# Expected output: 33 (ASCII value of '!')
print(ord('!'))
# Expected output: 64 (ASCII value of '@')
print(ord('@'))
# Expected output: 35 (ASCII value of '#')
print(ord('#'))
print("")

# Testing ord with whitespace characters
print("Testing ord with whitespace characters")
# Expected output: 32 (ASCII value of space ' ')
print(ord(' '))
# Expected output: 9 (ASCII value of tab '\t')
print(ord('\t'))
# Expected output: 10 (ASCII value of newline '\n')
print(ord('\n'))
print("")

# Testing ord with non-ASCII characters
print("Testing ord with non-ASCII characters")
# Expected output: 945 (Unicode code point of 'α')
print(ord('α'))
# Expected output: 233 (Unicode code point of 'é')
print(ord('é'))
# Expected output: 128512 (Unicode code point of 😀 emoji)
print(ord('😀'))
print("")