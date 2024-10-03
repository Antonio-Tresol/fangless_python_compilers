# basic examples
3 if 4 else 4
#"Yes" if True else "No"
#"Positive" if -1 > 0 else "Non-positive"
#"Pass" if (75,) >= (50,"a") else "Fail"
#"a" if "a" in "abc" else "not a"

# nested ternaries
"Found" if "x" in ["x", "y", "z",] else 3 if 4 else 4

# Deeply nested ternary
"Level 1" if True else "Level 2" if False else "Level 3" if True else "Level 4"
"Even" if 2 % 2 == 0 else "Odd" if 2 % 2 != 0 else "Unknown" if 2 % 2 == 1 else "Error"
"Positive" if -1 > 0 else "Non-positive" if -1 < 0 else "Zero" if -1 == 0 else "Negative"
"Adult" if 18 >= 18 else "Minor" if 18 < 18 else "Unknown" if 18 == 18 else "Error"
3 if 75 >= 50 else "Fail" if 75 < 50 else "Unknown" if 75 == 50 else "Error"