import time
import inspect

class KeepRunningTerminate(Exception): pass

def keeprunning(wait_secs=0, exit_on_success=False,
                    on_success=None, on_error=None, on_done=None):
    '''
    Keeps running a function running even on error.
    
    # Example 1: dosomething needs to run until completion condition
    # without needing to have a loop in its code. Also, when error
    # happens, we should NOT terminate execution
    
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
    
    
    # Example 2: In case you want to log exceptions while
    # dosomething keeps running, or perform any other action 
    # when an exceptions arise
    
    >>> def some_error(__exc__):
    ...     print (__exc__)
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
    division by zero
    AttrDict({'i': 3})
    AttrDict({'i': 4})
    Error happened
    division by zero
    AttrDict({'i': 5})
    AttrDict({'i': 6})
    Error happened
    division by zero
    AttrDict({'i': 7})
    Done
    
    # Example 3: Full set of arguments that can be passed in @keeprunning()
    # with class implementations
    
    >>> # Class that has some class variables
    ... class Demo(object):
    ...     SUCCESS_MSG = 'Yay!!'
    ...     DONE_MSG = 'STOPPED AT NOTHING!'
    ...     ERROR_MSG = 'Error'
    ...     
    ...     # Functions to be called by @keeprunning
    ...     def success(self):
    ...         print((self.SUCCESS_MSG))
    ...     
    ...     def failure(self, __exc__):
    ...         print((self.ERROR_MSG, __exc__))
    ...     
    ...     def task_done(self):
    ...         print((self.DONE_MSG))
    ...     
    ...     #Actual use of keeprunning with all arguments passed
    ...     @keeprunning(wait_secs=1, exit_on_success=False,
    ...             on_success=success, on_error=failure, on_done=task_done)
    ...     def dosomething(self, state):
    ...         state.i += 1
    ...         print (state)
    ...         if state.i % 2 == 0:
    ...             print("Error happened")
    ...             1 / 0 # create an error condition
    ...         if state.i >= 7:
    ...             print ("Done")
    ...             raise keeprunning.terminate
    ... 
    >>> demo = Demo()
    >>> state = AttrDict(i=0)
    >>> demo.dosomething(state)
    AttrDict({'i': 1})
    Yay!!
    AttrDict({'i': 2})
    Error happened
    ('Error', ZeroDivisionError('division by zero',))
    AttrDict({'i': 3})
    Yay!!
    AttrDict({'i': 4})
    Error happened
    ('Error', ZeroDivisionError('division by zero',))
    AttrDict({'i': 5})
    Yay!!
    AttrDict({'i': 6})
    Error happened
    ('Error', ZeroDivisionError('division by zero',))
    AttrDict({'i': 7})
    Done
    STOPPED AT NOTHING!
    '''
    def decfn(fn):

        def _call_callback(cb, fargs):
            if not cb: return
            # get the getargspec fn in inspect module (python 2/3 support)
            G = getattr(inspect, 'getfullargspec', getattr(inspect, 'getargspec'))
            cb_args = G(cb).args
            cb_args = dict([(a, fargs.get(a, None)) for a in cb_args])
            cb(**cb_args)

        def _fn(*args, **kwargs):
            fargs = inspect.getcallargs(fn, *args, **kwargs)
            fargs.update(dict(__fn__=fn, __exc__=None))

            while 1:
                try:
                    fn(*args, **kwargs)
                    if exit_on_success: break
                except (SystemExit, KeyboardInterrupt):
                    raise
                except KeepRunningTerminate:
                    break
                except Exception as exc:
                    fargs.update(dict(__exc__=exc))
                    _call_callback(on_error, fargs)
                    fargs.update(dict(__exc__=None))
                    if wait_secs: time.sleep(wait_secs)
                    continue

                _call_callback(on_success, fargs)
                
            _call_callback(on_done, fargs)

        return _fn

    return decfn

keeprunning.terminate = KeepRunningTerminate

