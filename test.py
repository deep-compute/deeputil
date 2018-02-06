#!/usr/bin/env python

import doctest
import unittest

from deeputil import *

#suite = doctest.DocTestSuite(deeputil)

def suite_maker():
    suite= unittest.TestSuite()
    suite.addTests(doctest.DocTestSuite(keep_running))
    suite.addTests(doctest.DocTestSuite(misc))
    suite.addTests(doctest.DocTestSuite(priority_dict))
    suite.addTests(doctest.DocTestSuite(timer))
    suite.addTests(doctest.DocTestSuite(streamcounter))
    return suite

if __name__ == "__main__":
    doctest.testmod(keep_running)
    doctest.testmod(misc, optionflags=doctest.ELLIPSIS)
    doctest.testmod(streamcounter)
    doctest.testmod(timer)
    doctest.testmod(priority_dict)
