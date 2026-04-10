# PyTypeInfo - Type checking typed objects at runtime.


## Introduction

How do you know if a duck is truly a duck? According to the Python interpreters logic of identifying objects the answer is:
"If it looks like a duck and quacks like a duck, it is probably a duck!". This dynamically "duck" typed approach is inherent to many interpreted languages. The type of an object at runtime is unknown. When an object is used, it must have all the properties required for the current execution. If not, the interpreter will throw an TypeError exception. 

Sometimes we want to know the type of an object during runtime. Python has a tool for it: `ìsinstance()`. This builtin function will tell you if an object is an instance of a class.

```python
class A:

    def __init__(self, initValue):
        self.value = initValue


foo = A(5)
isinstance(foo, A)
>>> True
```

This solution is fine (and fast). But it still lacks the type safety of a statically typed language. Let's add some type hints to our code.

```python
class A:

    def __init__(self, initValue: int):
        self.value: int = initValue


foo = A(5)
foo.value
>>> 5
isinstance(foo, A)
>>> True
foo.value + 5
>>> 10

bar = A('hi')
bar.value
>>> 'hi'
isinstance (bar, A)
>>> True
bar.value + 5

Traceback (most recent call last):
  File "<python-input>", line 1, in <module>
    bar.value + 5
    ~~~~~~~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

With our type hints we want to make sure that our objects value is an integer. Too bad type hints are ignored during execution. They are merely, as the name suggests, hints for other applications like static type checkers or code completion tools. That's why the interpreter is perfectly fine with assigning objects of any type to our instances 'value' property. When the interpreter is handling objects of type A it is sufficient that the 'value' property is present when accessing it. If the property itself has the correct type is becomes important when using it.

So how do we solve our problem? 

We could run an `isinstance()` check on every property access of our class. But nobody wants to write (or read) code like that.

That is where pytypeinfo comes into play. It is the solution to a lot of problems that occurred to me many times.

## A Simple Real Life Example

Let's say we have a class that represents a configuration of some kind. Maybe read from a configuration file or parsed from command line. We would like to know if the types of user supplied configuration values are correct. What i like to do is use Namedtuples as a way of representing immutable configurations. They are easily defined and can have default values.

```python
from typing import Namedtuple

class MyConfig(Namedtuple):
    value: int 1 = 0
    otherValue: str = 'Hello World'
```

With pytypeinfo it is possible to check the validity of instance member values.

```python
from pytypeinfo import TypeInfoCollection

# We create a TypeInfoCollection that contains type information of all 
# members
config_type_info = TypeInfoCollection(MyConfig)

# Type information for each member are available
config_type_info['value'].type
>>> <class 'int'>

# Checking a valid MyConfig instance returns True
conf_good = MyConfig(value=5, other_value='FooBar')
config_type_info.check(conf_good)
>>> True

# Checking an invalid MyConfig instance return False
conf_bad = MyConfig(value=5.5, other_value='FooBar')
config_type_info.check(conf_bad)
>>> False
```




