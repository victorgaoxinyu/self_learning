# OOP in Python

## Parent and Child Classes
```py
# parent class
class Person:
    ...

class Superhero(Person):
    ...

# visual representation of Superhero class
print(help(Superhero))
```

A child class will automatically inherit the `__init__` method if it is not defined. `__init__` is called when an object is instantiated, and `super()` does not need to be used.

```py
isinstance(obj, ClassName)
issubclass(subClassName, ClassName)
```

## Extending and Overriding
- Extending a class means that new attributes and methods are given to the child class.
- Overriding a method means to inherit a method from the parent class, keep its name, but change the contents of the method.

## Multiple Inheritance
```py
class Dinosaur:
  def __init__(self, size, weight):
    self.size = size
    self.weight = weight
    
class Carnivore:
  def __init__(self, diet):
    self.diet = diet

class Tyrannosaurus(Dinosaur, Carnivore):
    pass

# this wont work
tiny = Tyrannosaurus(12, 14, "whatever it wants")
print(tiny.size)

# this will work
tiny = Tyrannosaurus(12, 14)
print(tiny.size)

# OR... Override the __init__ method
class Tyrannosaurus(Dinosaur, Carnivore):
    def __init__(self, size, weight, diet):
        # this wont work, no idea who is super()
        # super().__init__(size, weight)
        # super().__init__(diet)
        Dinosaur.__init__(self, size, weight)
        Carnivore.__init__(self, diet)

# then you can init this class by...
tiny = Tyrannosaurus(12, 14, "whatever it wants")
```
Method Resolution Order (MRO)
```py
# class C(A, B):
#   pass
obj = C()
print(C.mro())
# [<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>]
```

## Encapsulation
- Encapsulation is a concept in which related data and methods are grouped together, and in which access to data is restricted.
- `public` and `private`

```py
class Phone:
  def __init__(self, model, storage, megapixels, carrier):
    self._model = model
    self._storage = storage
    self._megapixels = megapixels
    self._carrier = carrier
    
my_phone = Phone("iPhone", 256, 12, "AT&T")
print(my_phone.__dict__)
print(my_phone._model)
# Single Underscore is a convention
# an informal agreement for private
# not really mean private
```
Are Double Underscores Really Private?
- No. Double underscores were not added to the Python language to promote encapsulation. Rather, the double underscore is used to avoid name collisions in inheritance.
- When the Python interpreter encounters an attribute with a double underscore, it does not make it private. Instead, it changes the name to `_ClassName__AttributeName`

## Getter and Setter

