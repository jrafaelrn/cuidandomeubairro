import pandas as pd
import unittest
import os
import sys

path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
path = os.path.join(path, 'classes')
path = os.path.join(path, 'loader')

sys.path.insert(0, path)

from loader import Loader


class TestLoader(unittest.TestCase):

    load = Loader()

    def test_convert_row(self):
        
        row = []
        columns = ['a', 'b', 'c']
        returns = self.load.get_values_from_row(row, columns)
        self.assertEqual(returns, [None, None, None])


        

if __name__ == '__main__':
    unittest.main()