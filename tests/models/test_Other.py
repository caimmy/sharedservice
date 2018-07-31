# _*_ coding: utf-8 _*_
"""
-------------------------------------------------
File Name： test_Other
Description:
Author: caimmy
date： 2018/7/5
-------------------------------------------------
Change Activity:
2018/7/5
-------------------------------------------------
"""
__author__ = 'caimmy'

import unittest

class OtherTest(unittest.TestCase):
    def test_T(self):
        self.assertTrue(5 > 3, "abc")


if "__main__" == __name__:
    unittest.main()