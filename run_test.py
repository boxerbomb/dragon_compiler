import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'parser/')

import unittest

import parser

class TestStringMethods(unittest.TestCase):

    def test_iterativeFib(self):
        self.assertTrue(parser.runUnitTest("src_files/iterativeFib.src"))

    def test_logicals(self):
        self.assertTrue(parser.runUnitTest("src_files/logicals.src"))

    def test_multipleProcs(self):
        self.assertTrue(parser.runUnitTest("src_files/multipleProcs.src"))

    def test_math(self):
        self.assertTrue(parser.runUnitTest("src_files/math.src"))

    def test_recursiveFib(self):
        self.assertTrue(parser.runUnitTest("src_files/recursiveFib.src"))

    def test_source(self):
        self.assertTrue(parser.runUnitTest("src_files/source.src"))

    def test_test1b(self):
        self.assertTrue(parser.runUnitTest("src_files/test1b.src"))

    def test_test1(self):
        self.assertTrue(parser.runUnitTest("src_files/test1.src"))

    def test_test2(self):
        self.assertTrue(parser.runUnitTest("src_files/test2.src"))

    def test_test_heap(self):
        self.assertTrue(parser.runUnitTest("src_files/test_heap.src"))

    def test_test_program_minimal(self):
        self.assertTrue(parser.runUnitTest("src_files/test_program_minimal.src"))



if __name__ == '__main__':
    unittest.main()