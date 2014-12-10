"""
Copyright (C) 2014  Vahid Rafiei (@vahid_r)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest

from testbuilder.utils import get_version


class TestUtilsModuleFunctions(unittest.TestCase):
    """ This is a test skeleton for module-level functions at the utils module"""

    def test_version(self):
        self.assertEquals("0.9", get_version(), "The current version should be 0.9")
        
        


if __name__ == "__main__":
    unittest.main()