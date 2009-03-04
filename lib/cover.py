#!/usr/bin/env python
"""This script does a code coverage test.

Requires: http://nedbatchelder.com/code/modules/coverage.html
"""
import coverage
import unittest
import tests

coverage.erase()
coverage.start()

import c64
import c64.bytestream
import c64.formats
import c64.formats.basic
import c64.formats.bootsector
import c64.formats.d64
import c64.formats.petscii
import c64.formats.prg
import c64.formats.t64

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromNames(["tests"]))

testrunner = unittest.TextTestRunner()
testrunner.run(suite)

coverage.stop()
coverage.report([
    c64,
    c64.bytestream,
    c64.formats,
    c64.formats.basic,
    c64.formats.bootsector,
    c64.formats.d64,
    c64.formats.petscii,
    c64.formats.prg,
    c64.formats.t64,
    ])
