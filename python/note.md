# Python
Basic data types:
- Numeric
  - int
  - float
  - complex: <real_part> + <imaginary_part> j, 2+3j
- Sequeuce Type
  - String
  - List
  - Tuple
- Boolean
- Set
  - an unordered collection
- Dictionary
  - an unordered collection
  - key: value pair
- Binary Types
  - memoryview
  - bytearray
  - bytes


GIL:
Global interpreter lock

Operators:
```python
/  # float division
// # floor division
%  # modulus
** # power
```
Logical Operators:
```python
and, or, not
```
Bitwise Operators:
```python
& # bitwise AND
| # bitwise OR
~ # bitwise NOT
^ # bitwise XOR
>> # bitwise right shift
<< # bitwise left shift
```

Identity Operators

`is` and `is not` check if two values are located on the same part of memory. Two variables that are equal do not imply that they are identical.

### String
```py
slice(stop)
slice(start, stop, step)
```
prevent resolve escape
```py
s = "this\nis"
repr(s)
print(r"this\nis")
```

### Regex
```py
\ # drop special meaning of char following it
[] # char class
^ # matches the beginning
$ # matches the end
. # matches any char except newline
| # means OR
? # matches zero or one occurrence
* # any number of occurrences, including 0 occur
+ # one or more occur
{} # number of occur
() # enclose a group of regex
```

### List
```python
.append()
.insert(pos, val)
.extend() # add multiple elements
.reverse()
reversed()
.remove() # raise error is ele doesnt exist, only remove one element (first occur)
.pop()
.pop(idx)
.clear()
.index()
```

### Tuples
Concatenation: +

### Set
- unordered, mutable, no duplication

Append multiple elements
```python
test_set.update(up_ele)

test_set |= set(up_ele) # union

```

Remove items
```python
pop() # pop sml first
discard() # remove lrg first
remove(val)
```

contains element
```python
data = {...}
freq = Counter(data)

```

### Dict
Since py3.7, dict are ordered. 
```python
dict.get(key, default='None')
dict.items()  # a list of touple of each kv pair
dict.keys()
dict.values()
dict.update(dict2) # update dict with kv pair

```

### Control flow
Chaining comparison operators
```python
if a < b < c :
    {.....}
```
For loop
```python
range(start, end, step)

for fruit, color in zip(fruits, colors):
    ...

continue
pass
break
```
While loop
- usually used when num of iter is unknown

Sentinel Controlled Statement
```python
a = int(input('Enter a number (-1 to quit): ')) 

while a != -1: 
	a = int(input('Enter a number (-1 to quit): '))

```
Looping Techniques
```python
enumerate()
zip()
sorted()   # no value change, only display
reversed() # no value change, only display
```

### Functions
default argument
- once we have a default arg, all args to its right must have default vals

keyword args

positonal args

Arbitrary arguments:
- *arg: Non-keyword arguments
- **kwargs: Keyword arguments

Anonymous Functions
- use lambda to create
```python
cube = lambda x : x*x*x
```
- use lambda inside a function
```python
sorted(1, key=lambda x: int(x))

list(filter(lambda x: not (int(x) % 2 == 0 and int(x) > 0), l))

list(map(lambda x: str(int(x) + 10), l))
```

#### yield instead of return
- used in generators
- This allows its code to produce a series of values over time, rather than computing them at once and sending them back like a list.

#### First Class functions
- A function is an instance of the Object type.
- You can store the function in a variable.
- You can pass the function as a parameter to another function.
- You can return the function from a function.
- You can store them in data structures such as hash tables, lists, …

#### Decorators
- modify behaviour of class/function
- chaining decorators
  
```python
# decorator for func without return value
def calculate_time(func):
    def inner(*args, **kwargs):
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("Total time: ", func.__name__, end - begin)
    return inner1

@calculate_time
def factorial(num):
    time.sleep(2)
    print(math.factorial(num))

# decorator for func with return value
...
    returned_value = func(*args, **kwargs)
    ...
    return returned_value
...
```
#### Memoization using decorators
```python
memory = {}

def memoize_factorial(f):
    def inner(num):
        if num not in memory:
            memory[num] = f(num)

        return memory[num]

    return inner

@memoize_factorial
def factor(num):
    if num == 1:
        return 1
    else:
        return num * facto(num - 1)
```            


