# python f-strings

# f-strings are a feature of Python that allows you to embed expressions inside string literals, using
# the `f` prefix before the string. This allows you to easily format strings with variables and
# expressions.

# Here is an example of how to use f-strings:
name = "Alice"
age = 25
# Using f-strings to format a string with a variable and an expression
greeting = f"Hello , my name is {name} and I am {age} years old. "
print (greeting)
# Output: Hello , my name is Alice and I am 25 years old.

# Here is an example of Mathematical operations using  f-strings:
x = 5
y = 10
result = f"The sum of {x} and {y} is {x + y}."
print(result)
#The sum of 5 and 10 is 15.

# Here is an example of calling functions using  f-strings:
def greet(name):
    return f"Hello, {name}!"

name = "Bob"
message = f"{greet(name)} Welcome to the party."
print(message)
# Output: Hello, Bob! Welcome to the party.

# Here is an example of accessing attributes or dictionary keys using  f-strings:
user = {"name": "Carol", "age": 30}
message = f"{user['name']} is {user['age']} years old."
print(message)
#Carol is 30 years old.
