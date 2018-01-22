#!/usr/bin/env python

import doctest

from deeputil import *

#suite = doctest.DocTestSuite(misc)

if __name__ == "__main__":
    doctest.testmod(keeprunning)
    doctest.testmod(misc)
    doctest.testmod(streamcounter)
    doctest.testmod(timer)
    doctest.testmod(priority_dict)
