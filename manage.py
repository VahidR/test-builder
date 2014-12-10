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

import optparse
import sys
import unittest

from testbuilder.main import ConfigTestCreator 

def test():
    """Discover and Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
    
if __name__ == '__main__':
    help_message = "usage: python manage.py [options] arg"
    parser = optparse.OptionParser(help_message)
    parser.add_option('-t', '--test', dest='test', help='running tests')
    parser.add_option('-r', '--run', dest='run', help='running application')
    options, args = parser.parse_args()
    
    if len(sys.argv) < 2:
        print help_message
    if options.test:
        test()
    if options.run:
        print "Building the test configuration and uploading to loadimpact servers."
        print "........................................."
        ConfigTestCreator = ConfigTestCreator()
        ConfigTestCreator.send_user_scenario_string()
        ConfigTestCreator.create_and_send_test_config()
        print "Test configuration uploaded successfully !"
