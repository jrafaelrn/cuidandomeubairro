import pandas as pd
import unittest

from classes.city import lowercase_text


class TestCity(unittest.TestCase):

    def test_lowercase_text(self):
        
        data_frame_test = pd.DataFrame({"a": ["A", "b", "C"]})
        data_frame_test = lowercase_text(data_frame_test, "a")
        self.assertEqual(data_frame_test["a"][0], "a")
    