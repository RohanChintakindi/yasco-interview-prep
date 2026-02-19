# print("Hello")
# print(42)
# print()

# name = "Chint"
# age = 25
# height = 5.8
# is_student = True

# age = 26

# print(type(name))
# print(age)

# age = None

# print(f"{age} is of {type(age)}")

# greeting = "Hello"
# name = "Rohan"

# full = greeting + " " + name + "!"

# message = f"Hello, {name}! You are {age} years old!"
# print(f"{message.upper().lower()}")
# print(f"{message.strip().split(', ')}")
# print(f"{message.startswith('Hello')}")

# text = "  Hello, World!  "
# print(f"Original:  '{text}'")
# print(f"Strip:     '{text.strip()}'")      # Remove whitespace
# print(f"Lower:     '{text.strip().lower()}'")
# print(f"Upper:     '{text.strip().upper()}'")
# print(f"Replace:   '{text.strip().replace('World', 'Python')}'")
# print(f"Split:     {text.strip().split(', ')}")  # Split into list
# print(f"Starts with 'He': {text.strip().startswith('He')}")
# print()

# a = 10
# b = 3

# c = a + b
# c = a - b
# c = a * b
# c = a / b
# c = a // b
# c = a % b
# c = a ** b

# num_str = "42"
# num = int(num_str)

# pi_str = "3.14"
# pi = float(pi_str)

# back_to_str = str(pi_str)

# is_raining = True
# is_sunny = False
 
# and
# or
# not

# user_name = input("What's your name?")
# user_age = int(input("How old are you? "))

# if user_name and user_age:
#     print("bruh")

# age = 20

# if age>= 18:
#     print("You are an adult")
# elif age >= 13:
#     print("You are a teenager")
# else:
#     print("You are a child")

# temperature = 25
# is_sunny = True

# if temperature > 20 and is_sunny:
#     print("Perfect day for a walk!")
# elif temperature >20 or is_sunny:
#     print("Decent Day")
# else:
#     print("Stay inside")

# status = "adult" if age >= 18 else "minor"
# is_sunny = True if temperature > 20 else False

# print(is_sunny)

# fruits = ["apple", "banana","cherry"]

# for fruit in fruits:
#     print(f" I like {fruit}")

# for char in "Python":
#     print(f" Letter: {char}")

# for i in range(1,6,2):
#     print(i)

# for i,fruit  in enumerate(fruits):
#     print(i, fruit)

# person = {"name" : "Chintu", "age" : 25, "city" : "NYC"}
# for key, value in person.items():
#     print(key, value)

# count = 0
# while count < 5:
#     print(count)
#     count += 1

# for num in range(1,100):
#     if num == 5:
#         break

# for num in range(1,8):
#     if num % 2 == 0:
#         continue
#     print(f" Odd: {num}")

# for i in range(3):
#     pass

# # continue, pass and break

# for i in range(1,4):
#     for j in range(1,4):
#         print(f" {i} x {j} = {i * j}")

# numbers = [4, 2, 9, 1, 7, 3]
# maximum = numbers[0]
# for num in numbers:
#     if num > maximum:
#         maximum = num

# text = "Hello World"
# count = 0

# for char in text.lower():
#     if char in "aeiou":
#         count += 1

# print(count)

# for i in range(1,16):
#     if i % 3 == 0 and i % 5 == 0:
#         print(f" {i} : FizzBuzz")
#     elif i % 3 == 0:
#         print(f" {i}: Fizz")
#     elif i % 5 == 0:
#         print(f" {i}: Buzz")
#     else:
#         print(f" {i}")

# list -> ordered, mutable, allows duplicate
# dict -> key-value pairs, mutable
# tuple -> ordered, immutable, allows duplicates
# set -> unordered, mutable, no duplicates 

fruits = ["apple", "banana", "cherry"]
numbers = [1,2,3,4,5]