import os
import unittest

from pyutil import IOUtils
from .TestSupport import TestSupport


class test_IOUtils(unittest.TestCase):

    def test_has_dir(self):
        os.chdir(TestSupport.SUBJECTS_DIR)
        self.assertTrue(IOUtils.has_dir("sample-directory"))
        self.assertFalse(IOUtils.has_dir("none-existing-directory"))


if __name__ == '__main__':
    unittest.main()
