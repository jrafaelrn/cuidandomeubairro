import unittest
import os
import sys

path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
path = os.path.join(path, 'classes')
path = os.path.join(path, 'city')

sys.path.insert(0, path)

from locations import Localizer


class TestSearchLocations(unittest.TestCase):

    locator = Localizer()

    def test_fake_location(self):
        
        address = 'Rua Avenida Brasil, 123 - Bairro Centro - Cidade São Paulo - Estado São Paulo'
        city_name = 'São Paulo'
        self.assertEqual(self.locator.check_fake_location(address, city_name), False)

        address = 'Rua Avenida Brasil, 123 - Bairro Centro - Cidade Belo Horizonte - Estado Minas Gerais'
        city_name = 'São Paulo'
        self.assertEqual(self.locator.check_fake_location(address, city_name), True)

        address = 'Rua Avenida Brasil, 123 - Bairro Centro - Cidade Jundiaí - Estado São Paulo'
        city_name = 'Jundiaí'
        self.assertEqual(self.locator.check_fake_location(address, city_name), False)


if __name__ == '__main__':
    unittest.main()