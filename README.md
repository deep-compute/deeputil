# deeputil
Commonly re-used logic

## 
## Installation
> Prerequisites: Python3+
```
sudo pip install deeputil
```

## Usage

### Importing
```
import deeputil
```

```
>>> dir(deeputil)
['AttrDict', 'BlockTimer', 'Dummy', 'ExpiringCache', 'ExpiringCounter', 'FunctionTimer', 'IterAsFile', 'PriorityDict', 'StreamCounter', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', 'convert_ts', 'deepgetattr', 'generate_random_string', 'get_datetime', 'get_timestamp', 'keep_running', 'keeprunning', 'misc', 'parse_location', 'priority_dict', 'set_file_limits', 'streamcounter', 'timer', 'xcode']
```
### deeputil.misc module
```
>>> from deeputil import *
```
#### Generating random string of a specified length
```
>>> generate_random_string(length=10)
'76a4629edc'
```
#### Get current timestamp if @dt is None else return timestamp of @dt.
```
>>> t = datetime.datetime(2015, 05, 21)
>>> get_timestamp(t)
1432166400
```
#### Get datetime object from an epoch timestamp
```
>>> get_datetime(1432188772)
datetime.datetime(2015, 5, 21, 6, 12, 52)
```
 #### Get date epoch timestamp of any date format
 @tt: time.struct_time(tm_year=2012, tm_mon=10, tm_mday=23, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=297, tm_isdst=-1)
 ```
>>> tt = time.strptime("23.10.2012", "%d.%m.%Y")
>>> convert_ts(tt)
1350950400
```
 @tt: time.struct_time(tm_year=1513, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=1, tm_isdst=0)
```
>>> tt = time.strptime("1.1.1513", "%d.%m.%Y")
>>> convert_ts(tt)
0
>>> tt = 12
>>> convert_ts(tt)
 ```
 #### Convert utf-8 encoding to str object
 ```
 >>> xcode('hello')
'hello'
>>> xcode(u'hello')
'hello'
 ```
 #### Parse location to return ip (str), port (int)
    @loc can be of the format
    http://<ip/domain>[:<port>]
    eg: http://localhost:8888
        http://localhost/

```
>>> parse_location('http://localhost/', 6379)
('localhost', 6379)
>>> parse_location('http://localhost:8888', 6379)
('localhost', 8888)
```

 #### Expiring Cache
 Return value for key. If not in cache or expired, return default
 
 ```
>>> c = ExpiringCache(10, default_timeout=1)
>>> c.put('a', 100)
>>> c.get('a')
100
>>> time.sleep(1)
>>> c.get('a')
 ```
 #### Recurse through an attribute chain to get the ultimate value (obj/data/member/value).
 
 ```
 >>> class Universe(object):
...     def __init__(self, galaxy):
...             self.galaxy = galaxy
...
>>> class Galaxy(object):
...     def __init__(self, solarsystem):
...             self.solarsystem = solarsystem
...
>>> class SolarSystem(object):
...     def __init__(self, planet):
...             self.planet = planet
...
>>> class Planet(object):
...     def __init__(self, name):
...             self.name = name
...
>>> universe = Universe(Galaxy(SolarSystem(Planet('Earth'))))
>>> deepgetattr(universe, 'galaxy.solarsystem.planet.name')
'Earth'
>>> deepgetattr(universe, 'solarsystem.planet.name', default=TypeError)
<type 'exceptions.TypeError'>
 ```
 #### A dictionary with attribute-style access. It maps attribute access to the real dictionary
 In a plain old dict, we can store values against keys like this
 ```
>>> d = {}
>>> d['a'] = 10
>>> d['a']
10
 ```
 However, sometimes it is convenient to interact with a dict as though it is an object. eg: d.a = 10 and access as d.a. This does not work in a dict
```
>>> d = {}
>>> d.a = 10
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'a'
```

This is where you can use an `AttrDict`
```

>>> d = AttrDict()
>>> d.a = 1
>>> d.a
1

>>> d
AttrDict({'a': 1})

>>> d['b'] = 2
>>> d['b']
2
>>> d.b
2

>>> d
AttrDict({'a': 1, 'b': 2})

>>> repr(d)
"AttrDict({'a': 1, 'b': 2})"

>>> del d['a']
>>> d
AttrDict({'b': 2})

>>> dd = d.copy()
>>> dd
AttrDict({'b': 2})
```
#### Wrap an iterator in a file-like API
If you have a generator producing a list of strings, 'IterAsFile' could make it look like a file.
```
>>> def str_fn():
...     for c in 'a', 'b', 'c':
...             yield c * 3
...
>>> IAF = IterAsFile(str_fn())
>>> IAF.read(6)
'aaabbb'
>>> IAF.read(4)
'ccc'
>>> IAF.read(2)
```
#### ExpiringCounter

```
>>> c = ExpiringCounter(duration=1)
>>> c.put('name')
>>> c.get('name')
1
>>> time.sleep(2)
>>> c.get('name')
0
>>> c.put('name')
>>> c.put('name')
>>> c.get('name')
2
```

#### Dummy class
Abstraction that creates a dummy object
that does no-operations on method invocations
but logs all interactions

Let us create a dummy object and perform some random operations on it
```
>>> d = Dummy(1, a=5)
>>> d.foo()

>>> d.bar
<deeputil.misc.Dummy object at 0x...>

>>> d.foo.bar()
```
Now do the same as above but ask Dummy to print the activity
```
>>> d = Dummy(1, a=5, __quiet__=False)
(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': [], 'args': (1,), 'kwargs': {'a': 5}})
>>> d.foo() 
(<deeputil.misc.Dummy object at 0x...>, '__getattr__', {'attr': 'foo'})
(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': ['foo'], 'args': (), 'kwargs': {}})
(<deeputil.misc.Dummy object at 0x...>, '__call__', {'prefix': ['foo'], 'args': (), 'kwargs': {}})
>>> d.bar
(<deeputil.misc.Dummy object at 0x...>, '__getattr__', {'attr': 'bar'})
(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': ['bar'], 'args': (), 'kwargs': {}})
<deeputil.misc.Dummy object at 0x...>
>>> d.foo.bar()
(<deeputil.misc.Dummy object at 0x...>, '__getattr__', {'attr': 'foo'})
(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': ['foo'], 'args': (), 'kwargs': {}})
(<deeputil.misc.Dummy object at 0x...>, '__getattr__', {'attr': 'bar'})
(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': ['foo', 'bar'], 'args': (), 'kwargs': {}})
(<deeputil.misc.Dummy object at 0x...>, '__call__', {'prefix': ['foo', 'bar'], 'args': (), 'kwargs': {}})
````
### deeputil.keeprunning module
```
>>> from deeputil import keeprunning
```
#### Keeps running a function running even on error.

 Example 1: dosomething needs to run until completion condition without needing to have a loop in its code. Also, when error happens, we should NOT terminate execution
 
 ```
>>> from deeputil import AttrDict
>>> @keeprunning(wait_secs=1)
... def dosomething(state):
...     state.i += 1
...     print (state)
...     if state.i % 2 == 0:
...         print("Error happened")
...         1 / 0 # create an error condition
...     if state.i >= 7:
...         print ("Done")
...         raise keeprunning.terminate
... 
>>> state = AttrDict(i=0)
>>> dosomething(state)
AttrDict({'i': 1})
AttrDict({'i': 2})
Error happened
AttrDict({'i': 3})
AttrDict({'i': 4})
Error happened
AttrDict({'i': 5})
AttrDict({'i': 6})
Error happened
AttrDict({'i': 7})
Done
 ```
 Example 2: In case you want to log exceptions while dosomething keeps running, or perform any other action when an exceptions arise.
 ```
>>> def some_error(fn, args, kwargs, exc):
...     print (exc)
... 
>>> @keeprunning(on_error=some_error)
... def dosomething(state):
...     state.i += 1
...     print (state)
...     if state.i % 2 == 0:
...         print("Error happened")
...         1 / 0 # create an error condition
...     if state.i >= 7:
...         print ("Done")
...         raise keeprunning.terminate
... 

>>> state = AttrDict(i=0)
>>> dosomething(state)
AttrDict({'i': 1})
AttrDict({'i': 2})
Error happened
integer division or modulo by zero
AttrDict({'i': 3})
AttrDict({'i': 4})
Error happened
integer division or modulo by zero
AttrDict({'i': 5})
AttrDict({'i': 6})
Error happened
integer division or modulo by zero
AttrDict({'i': 7})
Done
 ```
 Example 3:Full set of arguments that can be passed in @keeprunning()
 
 ```
>>> def success(fn, args, kwargs):
...     print('yay!!')
... 
>>> def failure(fn, args, kwargs, exc):
...     print('fck!', exc)
... 
>>> def task_done(fn, args, kwargs):
...     print('STOPPED AT NOTHING!')
... 
>>> @keeprunning(wait_secs=1, exit_on_success=False,
...             on_success=success, on_error=failure, on_done=task_done)
... def dosomething(state):
...     state.i += 1
...     print (state)
...     if state.i % 2 == 0:
...         print("Error happened")
...         1 / 0 # create an error condition
...     if state.i >= 7:
...         print ("Done")
...         raise keeprunning.terminate
... 
>>> state = AttrDict(i=0)
>>> dosomething(state)
AttrDict({'i': 1})
yay!!
AttrDict({'i': 2})
Error happened
('fck!', ZeroDivisionError('integer division or modulo by zero',))
AttrDict({'i': 3})
yay!!
AttrDict({'i': 4})
Error happened
('fck!', ZeroDivisionError('integer division or modulo by zero',))
AttrDict({'i': 5})
yay!!
AttrDict({'i': 6})
Error happened
('fck!', ZeroDivisionError('integer division or modulo by zero',))
AttrDict({'i': 7})
Done
STOPPED AT NOTHING!
 ```
### deeputil.timer module
```
>>> from deeputil import BlockTimer
```
#### To check execution time of a block of code.
with Timer() as t:
`<code>`
print t.interval
```
>>> with BlockTimer() as t:
...     time.sleep(1)
...
>>> int(t.interval)
1
```
#### To check execution time of a function as follows:
```
>>> from deeputil import FunctionTimer
```

```
>>> def logger(details, args, kwargs): #some function that uses the time output
...     print(details)
... 
>>> @FunctionTimer(on_done= logger)
... def foo(t=10):
...     print 'foo executing...'
...     time.sleep(t)
... 
>>> @FunctionTimer(on_done= logger)
... def bar(t, n):
...     for i in range(n):
...             print 'bar executing...'
...             time.sleep(1)
...     foo(t)
... 
>>> bar(3,2)
bar executing...
bar executing...
foo executing...
('foo', 3)
('bar', 5)
```

### deeputil.streamingcounter module
```
>>> from deeputil import StreamCounter
```
### deeputil.priority_dict module
```
>>> from deeputil import PriorityDict
```
#### Dictionary that can be used as a priority queue.
Keys of the dictionary are items to be put into the queue, and values
are their respective priorities. All dictionary methods work as expected.
The advantage over a standard heapq-based priority queue is
that priorities of items can be efficiently updated (amortized O(1))
using code as 'thedict[item] = new_priority.'

The 'smallest' method can be used to return the object with lowest
priority, and 'pop_smallest' also removes it.

The 'sorted_iter' method provides a destructive sorted iterator.

```
>>> x = PriorityDict({'id1': 22, 'id2': 13, 'id3': 29, 'id4': 25, 'id5': 19})
>>> x.smallest()
'id2'
>>> x.pop_smallest()
'id2'
>>> x
{'id4': 25, 'id5': 19, 'id3': 29, 'id1': 22}
>>> x = PriorityDict({})
>>> x.smallest()
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "build/bdist.linux-x86_64/egg/rsslurp/priority_dict.py", line 83, in smallest
        v, k = heap[0]
IndexError: list index out of range
>>> x.pop_smallest()
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "build/bdist.linux-x86_64/egg/rsslurp/priority_dict.py", line 96, in pop_smallest
        v, k = heappop(heap)
IndexError: index out of range
```

