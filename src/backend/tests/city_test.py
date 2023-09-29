import pandas as pd
import unittest
import os
import sys

path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
path = os.path.join(path, 'classes')
path = os.path.join(path, 'city')

sys.path.insert(0, path)

from city import lowercase_text


class TestCity(unittest.TestCase):

    def test_lowercase_text(self):
        
        data_frame_test = pd.DataFrame({"a": ["A", "b", "C"]})
        data_frame_test = lowercase_text(data_frame_test, "a")
        self.assertEqual(data_frame_test["a"][0], "a")
    