# Testing input with a prompt (for text input)
print("Testing input with a prompt")
# User will input 'Hello'
# Expected output: 'Hello'
user_input = input("Enter something: ")
print(user_input)
print("")

# Testing input with numeric values (user inputs a number as string)
print("Testing input with numeric values")
# User will input '123'
# Expected output: '123' (input is always returned as a string)
user_input = input("Enter a number: ")
print(user_input)
print("")

# Testing input with float numbers (input as string, needs conversion)
print("Testing input with float numbers")
# User will input '3.14'
# Expected output: '3.14' (input is returned as string)
user_input = input("Enter a float: ")
print(user_input)
print("")

# Testing input with empty input
print("Testing input with empty input")
# User will input an empty string
# Expected output: '' (empty string)
user_input = input("Enter something (or press enter): ")
print(user_input)
print("")

# Testing input with a string containing special characters
print("Testing input with special characters")
# User will input '@$#%'
# Expected output: '@$#%' (input string will be returned as is)
user_input = input("Enter special characters: ")
print(user_input)
print("")

# Testing input when user provides whitespace
print("Testing input with leading/trailing spaces")
# User will input '   hello   '
# Expected output: '   hello   ' (input will retain spaces unless explicitly stripped)
user_input = input("Enter something with spaces: ")
print(user_input)
print("")

# Testing input with multiline input
print("Testing input with multiline input (simulated by using multiple inputs)")
# User will input 'First line' then 'Second line' (simulate multiple inputs)
# Expected output: 'First line', 'Second line'
user_input1 = input("Enter first line: ")
user_input2 = input("Enter second line: ")
print(user_input1)
print(user_input2)
print("")
