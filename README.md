# deeputil
Commonly re-used logic

## Installation
```

```
## Usage

## Importing
```
from deeputil import *
```
```
>>> dir(deeputil)
['StreamCounter', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', 'keeprunning', 'misc', 'priority_dict', 'streamcounter', 'timer']
```
### deeputil.misc module
```
>>> from deeputil.misc import *
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
```````````````````````````````````````
