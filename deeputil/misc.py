import time
import datetime
import calendar
import os
import inspect
import random
import string

import binascii
from functools import reduce

def generate_random_string(length=6):
    '''
    Returns a random string of a specified length.

    >>> len(generate_random_string(length=25))
    25

    # Test randomness. Try N times and observe no duplicaton
    >>> N = 100
    >>> len(set(generate_random_string(10) for i in range(N))) == N
    True
    '''
    n = int(length / 2 + 1)
    x = binascii.hexlify(os.urandom(n))
    return x[:length]

def get_timestamp(dt=None):
    '''
    Return current timestamp if @dt is None
    else return timestamp of @dt.

    >>> t = datetime.datetime(2015, 0o5, 21)
    >>> get_timestamp(t)
    1432166400
    '''
    if dt is None:
        dt = datetime.datetime.utcnow()

    t = dt.utctimetuple()
    return calendar.timegm(t)

def get_datetime(epoch):
    '''
    get datetime from an epoch timestamp
    >>> get_datetime(1432188772)
    datetime.datetime(2015, 5, 21, 6, 12, 52)
    '''
    t = time.gmtime(epoch)
    dt = datetime.datetime(*t[:6])
    return dt

def convert_ts(tt):
    '''
    # @tt: time.struct_time(tm_year=2012, tm_mon=10, tm_mday=23, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=297, tm_isdst=-1)
    >>> tt = time.strptime("23.10.2012", "%d.%m.%Y")
    >>> convert_ts(tt)
    1350950400

    # @tt: time.struct_time(tm_year=1513, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=1, tm_isdst=0)
    >>> tt = time.strptime("1.1.1513", "%d.%m.%Y")
    >>> convert_ts(tt)
    0
    >>> tt = 12
    >>> convert_ts(tt)
    '''
    try:
        ts = calendar.timegm(tt)

        '''
        As from the github issue https://github.com/prashanthellina/rsslurp/issues/680,
        there are some cases where we might get timestamp in negative values, so consider
        0 if the converted timestamp is negative value.
        '''
        if ts < 0: ts = 0
    except TypeError:
        ts = None
    return ts

#FIXME No unicde in python 3
def xcode(text, encoding='utf8', mode='ignore'):
    '''
    Converts unicode encoding to str
    >>> xcode(b'hello')
    b'hello'
    >>> xcode('hello')
    b'hello'
    '''
    return text.encode(encoding, mode) if isinstance(text, str) else text

from urllib.parse import urlparse

def parse_location(loc, default_port):
    '''
    @loc can be of the format
    http://<ip/domain>[:<port>]
    eg: http://localhost:8888
        http://localhost/
    return ip (str), port (int)
    >>> parse_location('http://localhost/', 6379)
    ('localhost', 6379)
    >>> parse_location('http://localhost:8888', 6379)
    ('localhost', 8888)
    '''

    parsed = urlparse(loc)

    if ':' in parsed.netloc:
        ip, port = parsed.netloc.split(':')
        port = int(port)
    else:
        ip, port = parsed.netloc, default_port

    return ip, port


from repoze.lru import ExpiringLRUCache
class ExpiringCache(ExpiringLRUCache):
    '''
    Return value for key. If not in cache or expired, return default
    >>> c = ExpiringCache(10, default_timeout=1)
    >>> c.put('a', 100)
    >>> c.get('a')
    100
    >>> time.sleep(1)
    >>> c.get('a')
    '''

    def get(self, key, default=None):
        self.lookups += 1
        try:
            pos, val, expires = self.data[key]
        except KeyError:
            self.misses += 1
            return default
        if expires > time.time():
            # cache entry still valid
            self.hits += 1
            # Not updating clock_refs to disable
            # LRU logic as we just want expiry withour LRU
            # self.clock_refs[pos] = True
            return val
        else:
            # cache entry has expired. Make sure the space in the cache can
            # be recycled soon.
            self.misses += 1
            self.clock_refs[pos] = False
            return default


def deepgetattr(obj, attr, default=AttributeError):
    """
    Recurses through an attribute chain to get the ultimate value (obj/data/member/value).
    From: http://pingfive.typepad.com/blog/2010/04/deep-getattr-python-function.html
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
    <class 'TypeError'>
    """
    try:
        return reduce(getattr, attr.split('.'), obj)
    except AttributeError:
        if default is not AttributeError:
            return default
        raise


class AttrDict(dict):
    '''
    A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.
    # from: http://code.activestate.com/recipes/473786-dictionary-with-attribute-style-access/

    In a plain old dict, we can store values against keys like this

    >>> d = {}
    >>> d['a'] = 10
    >>> d['a']
    10

    However, sometimes it is convenient to interact with a dict as
    though it is an object. eg: d.a = 10 and access as d.a. This does
    not work in a dict

    >>> d = {}
    >>> d.a = 10
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'dict' object has no attribute 'a'

    This is where you can use an `AttrDict`

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
    >>> del d['a']
    >>> d
    AttrDict({'b': 2})

    >>> dd = d.copy()
    >>> dd
    AttrDict({'b': 2})
    '''

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)

    def __getstate__(self):
        return list(self.__dict__.items())

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, name):
        item = super(AttrDict, self).__getitem__(name)
        return AttrDict(item) if isinstance(item, dict) else item

    def __delitem__(self, name):
        return super(AttrDict, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        ch = AttrDict(self)
        return ch

class IterAsFile(object):
    '''
    Wraps an iterator in a file-like API,
    i.e. if you have a generator producing a list of strings,
    this could make it look like a file.

    # http://stackoverflow.com/a/12593795/332313

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
    '''

    def __init__(self, it):
      self.it = it
      self.next_chunk = ''

    def _grow_chunk(self):
      self.next_chunk = self.next_chunk + next(self.it)

    def read(self, n):
      if self.next_chunk == None:
          return None

      try:
          while len(self.next_chunk) < n:
            self._grow_chunk()

          rv = self.next_chunk[:n]
          self.next_chunk = self.next_chunk[n:]
          return rv

      except StopIteration:
          rv = self.next_chunk
          self.next_chunk = None
          return rv

class LineReader(object):
    def __init__(self, it, linesep='\n'):
        self.parts = []
        self.it = it
        self.linesep = linesep

    def __iter__(self):
        for chunk in self.it:
            loc = end_loc = 0
            while loc <= len(chunk):
                end_loc = chunk.find(self.linesep, loc)
                if end_loc == -1:
                    self.parts.append(chunk[loc:])
                    break

                else:
                    yield ''.join(self.parts) + chunk[loc:end_loc+1]
                    self.parts = []
                    loc = end_loc + 1

        if self.parts:
            yield ''.join(self.parts)

from .priority_dict import PriorityDict
class ExpiringCounter(object):
    '''
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
    '''

    DEFAULT_DURATION = 60 #seconds

    def __init__(self, duration=DEFAULT_DURATION):
        self.duration = duration
        self.latest_ts = int(time.time())
        self.counts = PriorityDict()
        self.count = 0
        self.history = {}

    def put(self, key):
        self.update()

        ts = int(time.time())

        hcounts = self.history.get(ts, {})
        hcounts[key] = hcounts.get(key, 0) + 1
        self.history[ts] = hcounts

        self.counts[key] = self.counts.get(key, 0) + 1
        self.count += 1

    def get(self, key):
        self.update()
        return self.counts.get(key, 0)

    def update(self):
        ts = int(time.time() - self.duration)

        ts_keys = [x for x in self.history if x < ts]
        for ts_key in ts_keys:
            hcounts = self.history.pop(ts_key)

            for key, count in list(hcounts.items()):
                kcount = self.counts[key]
                kcount -= count
                if kcount <= 0: del self.counts[key]
                else: self.counts[key] = kcount
                self.count -= count

#TODO Examples and Readme.md
import resource
def set_file_limits(n):
    '''
    Set the limit on number of file descriptors
    that this process can open.

    '''

    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (n, n))
        return True
    except ValueError:
        return False

class Dummy(object):
    '''
    Abstraction that creates a dummy object
    that does no-operations on method invocations
    but logs all interactions

    # Let us create a dummy object and perform some
    # random operations on it

    >>> d = Dummy(1, a=5)
    >>> d.foo()

    >>> d.bar()

    >>> d.foo.bar()

    #Now do the same as above but ask Dummy to print the activity

    #>>> d = Dummy(1, a=5, __quiet__=False) # doctest: +ELLIPSIS
    #(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': [], 'args': (1,), 'kwargs': {'a': 5}})

    #>>> d.foo() # doctest: +ELLIPSIS
    #(<deeputil.misc.Dummy object at 0x...>, '__getattr__', {'attr': 'foo'})
    #(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': ['foo'], 'args': (), 'kwargs': {}})
    #(<deeputil.misc.Dummy object at 0x...>, '__call__', {'prefix': ['foo'], 'args': (), 'kwargs': {}})

    #>>> d.bar # doctest: +ELLIPSIS
    #(<deeputil.misc.Dummy object at 0x...>, '__getattr__', {'attr': 'bar'})
    #(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': ['bar'], 'args': (), 'kwargs': {}})
    #<deeputil.misc.Dummy object at 0x...>

    #>>> d.foo.bar() # doctest: +ELLIPSIS
    #(<deeputil.misc.Dummy object at 0x...>, '__getattr__', {'attr': 'foo'})
    #(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': ['foo'], 'args': (), 'kwargs': {}})
    #(<deeputil.misc.Dummy object at 0x...>, '__getattr__', {'attr': 'bar'})
    #(<deeputil.misc.Dummy object at 0x...>, '__init__', {'prefix': ['foo', 'bar'], 'args': (), 'kwargs': {}})
    #(<deeputil.misc.Dummy object at 0x...>, '__call__', {'prefix': ['foo', 'bar'], 'args': (), 'kwargs': {}})
    '''

    def _log(self, event, data):
        if not self._quiet:
            print((self, event, data))

    def __init__(self, *args, **kwargs):
        self._prefix = kwargs.pop('__prefix__', [])
        self._quiet = kwargs.pop('__quiet__', True)
        self._log('__init__', dict(args=args, kwargs=kwargs, prefix=self._prefix))

    def __getattr__(self, attr):
        if attr == '__wrapped__':
            raise AttributeError

        self._log('__getattr__', dict(attr=attr))
        return Dummy(__prefix__=self._prefix + [attr], __quiet__=self._quiet)

    def __call__(self, *args, **kwargs):
        self._log('__call__', dict(args=args, kwargs=kwargs, prefix=self._prefix))


