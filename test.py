#!/usr/bin/env python

import doctest
import unittest

from deeputil import *

def suite_maker():
    suite = unittest.TestSuite()
    suite.addTests(doctest.DocTestSuite(keeprunning))
    suite.addTests(doctest.DocTestSuite(misc))
    suite.addTests(doctest.DocTestSuite(priority_dict))
    suite.addTests(doctest.DocTestSuite(timer))
    suite.addTests(doctest.DocTestSuite(streamcounter))
    return suite

if __name__ == "__main__":
    doctest.testmod(keeprunning)
    doctest.testmod(misc)
    doctest.testmod(streamcounter)
    doctest.testmod(timer)
    doctest.testmod(priority_dict)
