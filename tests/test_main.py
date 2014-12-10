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
import types
import loadimpact
import datetime

from testbuilder import JMXParse, ConfigTestCreator
from config import basedir, client



class TestJMXParse(unittest.TestCase):
    """ This is a test skeleton for JMXParse class. """
    def setUp(self):
        self.jmxParse = JMXParse()
    
    def tearDown(self):
        del self.jmxParse

    def test_if_assets_folder_exits(self):
        """ tests if the 'assests' folder exists in project root """
        self.assertTrue(self.jmxParse._validate_assets_folder("assets"), 
                        "The 'assests' folder does not exit !") 
        
    def test_if_Jmetertestplan_exists(self):
        """ 
         tests if the 'Jmetertestplan.jmx' file exists in assests folder 
        """
        self.assertTrue(self.jmxParse._validate_jmx_file("Jmetertestplan.jmx"), 
                        "The Jmetertestplan.jmx file does not exit !")
        
    def test_fetch_filename(self):
        """
         checks if the full path to JMX file has been built correctly
        """
        self.assertEquals(basedir + "/assets/" + "Jmetertestplan.jmx" , 
                          self.jmxParse._fetch_jmx_file()) 
        
    def test_parse_and_build_jMeter_dict(self):
        """
         checks the created a dict() from JMX file, has the correct "type"
         and valid "entities". 
        """
        self.assertTrue(isinstance(self.jmxParse.parse_and_build_jMeter_dict(), types.DictType), 
                        "The return of parse_and_build_jMeter_dict() should be dict !") 
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("domain"), 
                        "There is the domain key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("concurrentPool"), 
                        "There is the concurrentPool key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("news_path"), 
                        "There is the news_path key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("testname"), 
                        "There is the testname key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("root_path"), 
                        "There is the root_path_one key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("method"), 
                        "There is the method key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("ramp_time"), 
                        "There is the ramp_time key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("coin_path"), 
                        "There is the coin_path key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("arg_value"), 
                        "There is the arg_value key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("arg_name"), 
                        "There is the arg_name key in the payload")
        self.assertTrue(self.jmxParse.parse_and_build_jMeter_dict().has_key("VUs"), 
                        "There is the VUs key in the payload")


class TestUserScenarioCreator(unittest.TestCase):
    """ This is a test skeleton for UserScenarioCreator class. """
    def setUp(self):
        self.userStoryClass = ConfigTestCreator()
        self.senario_payload = self.userStoryClass.send_user_scenario_string()
    
    def tearDown(self):
        user_story = client.get_user_scenario(self.senario_payload.id)
        user_story.delete()
        del self.userStoryClass

        
    def test_build_user_scenario_string(self):
        """
         Checks the sanity of the created lua-based string.
         Both its "type" and "entities".
        """
        self.assertTrue(isinstance(self.userStoryClass.build_user_scenario_string(), basestring), 
                        "The return of build_user_scenario_string() should be String !")  
        self.assertRegexpMatches(self.userStoryClass.build_user_scenario_string(), r"http\.request_batch", 
                                 "http.request_batch expression must exist in the payload string")
        
        self.assertRegexpMatches(self.userStoryClass.build_user_scenario_string(), r"GET", 
                      "GET method must exist in payload string") 
        self.assertRegexpMatches(self.userStoryClass.build_user_scenario_string(), r"client\.sleep\(10\)", 
                      "'client.sleep(10)' method must exist in the payload string") 
        self.assertRegexpMatches(self.userStoryClass.build_user_scenario_string(), r"test\.loadimpact\.com", 
                      "'test.loadimpact.com' field must exist in the payload string") 
        self.assertRegexpMatches(self.userStoryClass.build_user_scenario_string(), r"test\.loadimpact\.com/news\.php", 
                      "'test.loadimpact.com/news.php' field must exist in the payload string") 
        self.assertRegexpMatches(self.userStoryClass.build_user_scenario_string(), r"test\.loadimpact.\com/flip_coin.php\?bet=heads", 
                      "'test.loadimpact.com/flip_coin.php?bet=heads' field must exist in the payload string") 
        
        
    def test_send_user_scenario_string(self):
        """
         Tests the response of the sent user scenario.
         Both the "type" of response and its relevant "entities". 
        """
        self.assertTrue(isinstance(self.senario_payload, loadimpact.resources.UserScenario), 
                        "The return of send_user_scenario_string() should be in type of loadimpact.resources.UserScenario !")
        self.assertTrue(isinstance(self.senario_payload.id, types.IntType), "payload.id is an 'int' field")
        self.assertTrue(isinstance(self.senario_payload.data_stores, types.ListType), "data_stores is a list field")
        self.assertTrue(isinstance(self.senario_payload.load_script, basestring), "load_script is a string field")
        self.assertTrue(isinstance(self.senario_payload.name, basestring), "name is a string field")
        self.assertTrue(isinstance(self.senario_payload.updated, datetime.datetime), "name is a string field")
        self.assertEquals(self.senario_payload.script_type, 'lua', "script_type is 'lua'")


if __name__ == "__main__":
    unittest.main()