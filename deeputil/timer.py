import time

class FunctionTimerTerminate(Exception): pass

def FunctionTimer(on_done=None):
    '''
    # borrowed from https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
    To check execution time of a function as follows:
    >>> def logger(details, args, kwargs): #some function that uses the time output
    ...     print(details)
    ... 
    >>> @FunctionTimer(on_done= logger)
    ... def foo(t=10):
    ...     print('foo executing...')
    ...     time.sleep(t)
    ... 
    >>> @FunctionTimer(on_done= logger)
    ... def bar(t, n):
    ...     for i in range(n):
    ...             print('bar executing...')
    ...             time.sleep(1)
    ...     foo(t)
    ... 
    >>> bar(3,2)
    bar executing...
    bar executing...
    foo executing...
    ('foo', 3)
    ('bar', 5)
    '''
    def decfn(fn):

        def timed(*args, **kwargs):
            ts = time.time()
            result = fn(*args, **kwargs)
            te = time.time()
            if on_done:
                on_done((fn.__name__,int(te - ts)), args, kwargs)
            else:
                print(('%r  %d sec(s)' % \
                      (fn.__name__, (te - ts))))
            return result

        return timed

    return decfn

FunctionTimer.terminate = FunctionTimerTerminate

class BlockTimer:
    '''
    # borrowed from: http://preshing.com/20110924/timing-your-code-using-pythons-with-statement/
    To check execution time of a code.
    Time blocks of code as follows:
    with Timer() as t:
        <code>
    print t.interval
    >>> with Timer.block() as t:
    ...     time.sleep(1)
    ...
    >>> int(t.interval)
    1
    '''

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start

class Timer(object):
    decorator = staticmethod(FunctionTimer)
    block = BlockTimer


