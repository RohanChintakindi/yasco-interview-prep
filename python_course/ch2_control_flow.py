"""
=====================================================
 CHAPTER 2: CONTROL FLOW - IF/ELSE & LOOPS
=====================================================

Programs need to make DECISIONS and REPEAT actions.

  Decision:  "If it's raining, take an umbrella. Otherwise, wear sunglasses."
  Repeat:    "Send a reminder email to every user in the list."

Control flow is HOW you tell Python to do these things.


HOW TO RUN:
  python ch2_control_flow.py
"""

# =============================================================================
# PART 1: IF / ELIF / ELSE
# =============================================================================
#
# if checks a condition. If True, run the indented block.
# elif (else if) checks another condition.
# else runs if nothing above was True.
#
# INDENTATION MATTERS in Python! The indented code is "inside" the if.

print("=" * 40)
print("PART 1: if / elif / else")
print("=" * 40)

age = 20

if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager")
else:
    print("You are a child")

# You can chain multiple conditions with and / or:
temperature = 25
is_sunny = True

if temperature > 20 and is_sunny:
    print("Perfect day for a walk!")
elif temperature > 20 or is_sunny:
    print("Decent day")
else:
    print("Stay inside")

print()

# TERNARY (one-line if/else):
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")
print()


# =============================================================================
# PART 2: FOR LOOPS - REPEATING OVER A SEQUENCE
# =============================================================================
#
# for repeats code for EACH ITEM in a sequence (list, string, range, etc.)

print("=" * 40)
print("PART 2: for loops")
print("=" * 40)

# Loop through a list:
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"  I like {fruit}")
print()

# Loop through a string:
for char in "Python":
    print(f"  Letter: {char}")
print()

# range() generates numbers:
# range(5)      -> 0, 1, 2, 3, 4
# range(2, 6)   -> 2, 3, 4, 5
# range(0, 10, 2) -> 0, 2, 4, 6, 8  (step by 2)

print("Counting to 5:")
for i in range(1, 6):
    print(f"  {i}")
print()

# enumerate() gives you the INDEX and VALUE:
languages = ["Python", "JavaScript", "Rust"]
for index, lang in enumerate(languages):
    print(f"  {index}: {lang}")
print()

# Loop with a dict:
person = {"name": "Chint", "age": 25, "city": "NYC"}
for key, value in person.items():
    print(f"  {key}: {value}")
print()


# =============================================================================
# PART 3: WHILE LOOPS - REPEAT UNTIL A CONDITION IS FALSE
# =============================================================================
#
# while keeps running as long as the condition is True.
# BE CAREFUL: if the condition never becomes False, it runs FOREVER.

print("=" * 40)
print("PART 3: while loops")
print("=" * 40)

count = 0
while count < 5:
    print(f"  Count: {count}")
    count += 1  # count = count + 1 (MUST change the condition!)
print()

# Countdown:
n = 3
while n > 0:
    print(f"  {n}...")
    n -= 1
print("  Go!")
print()


# =============================================================================
# PART 4: BREAK, CONTINUE, PASS
# =============================================================================
#
# break:    EXIT the loop immediately
# continue: SKIP to the next iteration
# pass:     Do nothing (placeholder)

print("=" * 40)
print("PART 4: break, continue, pass")
print("=" * 40)

# break: stop when we find what we're looking for
print("break example:")
for num in range(1, 100):
    if num == 5:
        print(f"  Found 5! Stopping.")
        break
    print(f"  Checking {num}...")
print()

# continue: skip even numbers
print("continue example (skip evens):")
for num in range(1, 8):
    if num % 2 == 0:
        continue  # Skip this iteration
    print(f"  Odd: {num}")
print()

# pass: placeholder for code you haven't written yet
for i in range(3):
    pass  # TODO: implement later


# =============================================================================
# PART 5: NESTED LOOPS
# =============================================================================

print("=" * 40)
print("PART 5: Nested loops")
print("=" * 40)

# Multiplication table:
for i in range(1, 4):
    for j in range(1, 4):
        print(f"  {i} x {j} = {i * j}")
    print()  # Blank line between groups


# =============================================================================
# PART 6: PRACTICAL EXAMPLES
# =============================================================================

print("=" * 40)
print("PART 6: Practical examples")
print("=" * 40)

# Find the max in a list:
numbers = [4, 2, 9, 1, 7, 3]
maximum = numbers[0]
for num in numbers:
    if num > maximum:
        maximum = num
print(f"Max of {numbers} = {maximum}")

# Count vowels in a string:
text = "Hello World"
vowels = 0
for char in text.lower():
    if char in "aeiou":
        vowels += 1
print(f"Vowels in '{text}': {vowels}")

# FizzBuzz:
print("\nFizzBuzz (1-15):")
for i in range(1, 16):
    if i % 3 == 0 and i % 5 == 0:
        print(f"  {i}: FizzBuzz")
    elif i % 3 == 0:
        print(f"  {i}: Fizz")
    elif i % 5 == 0:
        print(f"  {i}: Buzz")
    else:
        print(f"  {i}")
print()


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# if condition:         for item in sequence:      while condition:
#     ...                   ...                        ...
# elif condition:       for i in range(n):
#     ...                   ...
# else:                 for i, v in enumerate(lst):
#     ...                   ...
#
# break     -> exit loop
# continue  -> skip to next iteration
# range(n)  -> 0 to n-1
# range(a, b, step) -> a to b-1, stepping by step
#
# =============================================================================
