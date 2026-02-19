"""
=====================================================
 CHAPTER 5: CLASSES & OBJECT-ORIENTED PROGRAMMING
=====================================================

WHAT IS OOP?
------------
Object-Oriented Programming organizes code around OBJECTS.
An object bundles DATA (attributes) and BEHAVIOR (methods) together.

Think of a real-world object: a Dog.
  DATA: name, breed, age, color
  BEHAVIOR: bark(), eat(), sleep()

In Python:
  class Dog:
      def __init__(self, name, breed):
          self.name = name      # data
          self.breed = breed    # data

      def bark(self):           # behavior
          print(f"{self.name} says Woof!")

A CLASS is the BLUEPRINT (template).
An OBJECT is an INSTANCE (specific thing created from the blueprint).

  class Dog:         <- blueprint (can make infinite dogs)
  buddy = Dog(...)   <- instance (one specific dog named Buddy)
  rex = Dog(...)     <- instance (another specific dog named Rex)


HOW TO RUN:
  python ch5_classes_and_oop.py
"""

# =============================================================================
# PART 1: BASIC CLASSES
# =============================================================================

print("=" * 40)
print("PART 1: Basic classes")
print("=" * 40)


class Dog:
    """A simple Dog class."""

    # __init__ is the CONSTRUCTOR - runs when you create a new Dog
    # self refers to the SPECIFIC instance being created
    def __init__(self, name, breed, age):
        self.name = name      # self.name = this dog's name
        self.breed = breed
        self.age = age

    def bark(self):
        """Dogs bark!"""
        print(f"{self.name} says: Woof!")

    def describe(self):
        return f"{self.name} is a {self.age}-year-old {self.breed}"


# Creating INSTANCES (objects):
buddy = Dog("Buddy", "Golden Retriever", 3)
rex = Dog("Rex", "German Shepherd", 5)

# Using the objects:
buddy.bark()                       # Buddy says: Woof!
print(buddy.describe())            # Buddy is a 3-year-old Golden Retriever
print(f"Rex's breed: {rex.breed}") # Accessing attributes
print()


# =============================================================================
# PART 2: SELF - WHAT IS IT?
# =============================================================================
#
# `self` is the instance itself. When you call buddy.bark(),
# Python automatically passes buddy as `self`.
#
#   buddy.bark()  is actually  Dog.bark(buddy)
#
# self.name on buddy -> buddy's name
# self.name on rex -> rex's name
#
# Every method needs self as the first parameter. Python fills it in
# automatically - you never pass it manually.


# =============================================================================
# PART 3: CLASS vs INSTANCE ATTRIBUTES
# =============================================================================

print("=" * 40)
print("PART 3: Class vs Instance attributes")
print("=" * 40)


class Cat:
    species = "Felis catus"  # CLASS attribute (shared by ALL cats)

    def __init__(self, name):
        self.name = name     # INSTANCE attribute (unique per cat)


whiskers = Cat("Whiskers")
luna = Cat("Luna")

print(f"Whiskers species: {whiskers.species}")  # Shared
print(f"Luna species: {luna.species}")            # Same
print(f"Whiskers name: {whiskers.name}")          # Unique
print(f"Luna name: {luna.name}")                  # Different
print()


# =============================================================================
# PART 4: INHERITANCE - BUILDING ON EXISTING CLASSES
# =============================================================================
#
# Inheritance lets you create a new class BASED ON an existing one.
# The new class (child) gets all the methods of the parent, and can
# add new ones or override existing ones.

print("=" * 40)
print("PART 4: Inheritance")
print("=" * 40)


class Animal:
    """Parent class."""
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        print(f"{self.name} says {self.sound}!")

    def __str__(self):
        return f"Animal({self.name})"


class Dog(Animal):  # Dog INHERITS from Animal
    """Child class - gets everything from Animal, plus dog-specific stuff."""
    def __init__(self, name, breed):
        super().__init__(name, "Woof")  # Call parent's __init__
        self.breed = breed              # Add dog-specific attribute

    def fetch(self):
        print(f"{self.name} fetches the ball!")


class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow")

    def purr(self):
        print(f"{self.name} purrs...")


dog = Dog("Buddy", "Labrador")
cat = Cat("Whiskers")

dog.speak()   # Inherited from Animal: "Buddy says Woof!"
dog.fetch()   # Dog-specific: "Buddy fetches the ball!"
cat.speak()   # Inherited from Animal: "Whiskers says Meow!"
cat.purr()    # Cat-specific: "Whiskers purrs..."
print()


# =============================================================================
# PART 5: DUNDER METHODS (MAGIC METHODS)
# =============================================================================
#
# Methods with double underscores (__name__) are "dunder" (double-under) methods.
# Python calls them automatically in certain situations.

print("=" * 40)
print("PART 5: Dunder methods")
print("=" * 40)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """Called by print() and str()."""
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        """Called in the REPL and by repr(). Should be unambiguous."""
        return f"Vector(x={self.x}, y={self.y})"

    def __add__(self, other):
        """Called when you use + between two Vectors."""
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self):
        """Called by len()."""
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

    def __eq__(self, other):
        """Called when you use == between two Vectors."""
        return self.x == other.x and self.y == other.y


v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1: {v1}")           # __str__
print(f"v1 + v2: {v1 + v2}") # __add__
print(f"v1 == v2: {v1 == v2}")  # __eq__
print(f"Vector(3,4) == Vector(3,4): {Vector(3,4) == Vector(3,4)}")
print()


# =============================================================================
# PART 6: PRACTICAL EXAMPLE - BANK ACCOUNT
# =============================================================================

print("=" * 40)
print("PART 6: Practical - Bank Account")
print("=" * 40)


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit must be positive!")
            return
        self.balance += amount
        self.transactions.append(f"+${amount}")
        print(f"Deposited ${amount}. Balance: ${self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Insufficient funds! Balance: ${self.balance}")
            return
        self.balance -= amount
        self.transactions.append(f"-${amount}")
        print(f"Withdrew ${amount}. Balance: ${self.balance}")

    def __str__(self):
        return f"Account({self.owner}, ${self.balance})"


account = BankAccount("Chint", 100)
account.deposit(50)
account.withdraw(30)
account.withdraw(200)  # Should fail
print(f"Transactions: {account.transactions}")
print()


# =============================================================================
# QUICK REFERENCE
# =============================================================================
#
# class MyClass:
#     class_attr = "shared"              # Class attribute
#
#     def __init__(self, x):             # Constructor
#         self.x = x                     # Instance attribute
#
#     def method(self):                  # Instance method
#         return self.x
#
#     def __str__(self): ...             # print(obj)
#     def __repr__(self): ...            # repr(obj)
#     def __eq__(self, other): ...       # obj1 == obj2
#     def __add__(self, other): ...      # obj1 + obj2
#     def __len__(self): ...             # len(obj)
#
# Inheritance:
#     class Child(Parent):
#         def __init__(self):
#             super().__init__()
#
# =============================================================================
