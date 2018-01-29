import time

class KeepRunningTerminate(Exception): pass

def keeprunning(wait_secs=0, exit_on_success=False,
                    on_success=None, on_error=None, on_done=None):
    '''
    Keeps running a function running even on error.
    
    # Example 1: dosomething needs to run until completion condition
    # without needing to have a loop in its code. Also, when error
    # happens, we should NOT terminate execution
    
    >>> from deeputil.misc import AttrDict
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
    
    
    # Example 2: In case you want to log exceptions while
    # dosomething keeps running, or perform any other action 
    # when an exceptions arise
    
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
    
    
    # Example 3:Full set of arguments that can be passed in @keeprunning()
    
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
    >>> 
    '''
    def decfn(fn):

        def _fn(*args, **kwargs):
            while 1:
                try:
                    fn(*args, **kwargs)
                    if exit_on_success: break
                except (SystemExit, KeyboardInterrupt):
                    raise
                except KeepRunningTerminate:
                    break
                except Exception, exc:
                    if on_error:
                        on_error(fn, args, kwargs, exc)
                    if wait_secs: time.sleep(wait_secs)
                    continue

                if on_success:
                    on_success(fn, args, kwargs)
                    
            if on_done:
                on_done(fn, args, kwargs)

        return _fn

    return decfn

keeprunning.terminate = KeepRunningTerminate

