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

import os
from xml.dom import minidom
import json
import requests

from config import basedir , client , api_token
from testbuilder.exceptions import ValidationError
from loadimpact import LoadZone


class JMXParse(object):
    """ 
     JMXParse class is responsible for parsing the JMX file, and returning
     the the required fields to build the test config
    """
    
    def __init__(self, filename = None , foldername = None):
        self.filename = filename
        self.foldername = foldername
        
    def _validate_jmx_file(self, filename):
        """ 
        validates the jmx file on the assests folder
        :param filename: the filename
         :return boolean state 
        """
        assets_folder = basedir + "/assets"
        return os.path.isfile(assets_folder + "/" + filename) 
    
    def _validate_assets_folder(self, foldername):
        """ 
        validate the assests folder on the root directory 
        :param foldername: the foldername
        :return boolean state 
        """
        return os.path.exists(basedir + "/" + foldername)
    
    def _fetch_jmx_file(self):
        """ 
        concatenate the file and folder together and returns the absolute path
        :return the absolute path of JMX file
        """
        return basedir + "/assets/" + "Jmetertestplan.jmx" 
    
    
    def parse_and_build_jMeter_dict(self):
        """ 
        this method fetched the "JMX file" in the assests folder, and 
        uses minidom xml library to parse it.
        
        OBS. minidom xml library has been used for its intuitive syntax and as 
        JMX file was  small enough to not to be worried about the performane. 
        "lxml" and "cElementTree" are two samples of high performance libs..
           
        :return jMeter_dict : a dictionary consisting the important fields in JMX file
        """
         
        if not self._validate_assets_folder("assets") and not self._validate_jmx_file("Jmetertestplan.jmx") :
            raise ValidationError("The file <Jmetertestplan.jmx> does not exist")
        
        jmx_file = self._fetch_jmx_file()
        jmx_xml = minidom.parse(jmx_file)
        jMeter_dict = {}

        testPlan_list = jmx_xml.getElementsByTagName("TestPlan")
        jMeter_dict['testname'] = testPlan_list[0].attributes["testname"].value
        
        stringProp_nodes = jmx_xml.getElementsByTagName("stringProp") # list of nodes
        
        for node in stringProp_nodes:
            if node.attributes.get("name").value == "ThreadGroup.num_threads" and node.firstChild is not None:
                jMeter_dict['VUs'] = node.firstChild.data
            if node.attributes.get("name").value == "ThreadGroup.ramp_time" and node.firstChild is not None:
                jMeter_dict['ramp_time'] = node.firstChild.data
            if node.attributes.get("name").value == "HTTPSampler.domain" and node.firstChild is not None:
                jMeter_dict['domain'] = node.firstChild.data
            if node.attributes.get("name").value == "HTTPSampler.concurrentPool" and node.firstChild is not None:
                jMeter_dict['concurrentPool'] = node.firstChild.data
            if node.attributes.get("name").value == "HTTPSampler.path" and node.firstChild is not None \
                                                                        and node.firstChild.data == "/":
                jMeter_dict['root_path'] = node.firstChild.data
            if node.attributes.get("name").value == "HTTPSampler.method" and node.firstChild is not None \
                                                                        and node.firstChild.data == "GET":
                jMeter_dict['method'] = node.firstChild.data
            if node.attributes.get("name").value == "HTTPSampler.path" and node.firstChild is not None \
                                                                    and node.firstChild.data == "/news.php":
                jMeter_dict['news_path'] = node.firstChild.data
            if node.attributes.get("name").value == "HTTPSampler.path" and node.firstChild is not None \
                                                                    and node.firstChild.data == "/flip_coin.php":
                jMeter_dict['coin_path'] = node.firstChild.data
            if node.attributes.get("name").value == "Argument.name" and node.firstChild is not None:
                jMeter_dict['arg_name'] = node.firstChild.data
            if node.attributes.get("name").value == "Argument.value" and node.firstChild is not None:
                jMeter_dict['arg_value'] = node.firstChild.data
        
        return jMeter_dict

            
class ConfigTestCreator(object):
    """ 
     ConfigTestCreator class has three important methods:
      1. build_user_scenario_string() builds a "lua-syntax" user scenario string 
      2. send_user_scenario_string() builds a user scenario and sends a RESTful 
         message to the loadimpact server
      3. create_and_send_test_config() builds a test configuration and sends 
         a RESTful message to the loadimpact server
    """
    def __init__(self):
        self.parserClass = JMXParse()
    
    def build_user_scenario_string(self):
        """ 
         builds a "lua-syntax" user scenario string 
         :return a string representation of user scenario
        """
        dict_data= self.parserClass.parse_and_build_jMeter_dict()
         
        # using docstring to easily escape the double quotes.. 
        userscenario_string = '''''' 
        userscenario_string += '''http.request_batch({'''
        userscenario_string += '''{"''' + dict_data.get("method") + '''", '''
        userscenario_string += '''"http://''' + dict_data.get("domain") + dict_data.get("root_path") + '''"},'''
        userscenario_string += '''{"''' + dict_data.get("method") + '''", '''
        userscenario_string += '''"http://''' + dict_data.get("domain") + dict_data.get("news_path") + '''"}})'''
        
        userscenario_string += ''' client.sleep(10) '''

        userscenario_string += '''http.request_batch({'''
        userscenario_string += '''{"''' + dict_data.get("method") + '''", '''
        userscenario_string += '''"http://''' + dict_data.get("domain") + dict_data.get("coin_path") + '''"},'''
        userscenario_string += '''{"''' + dict_data.get("method") + '''", '''
        userscenario_string += '''"http://''' + dict_data.get("domain") + dict_data.get("coin_path") +  \
                            '''?''' + dict_data.get("arg_name") + '''=''' + dict_data.get("arg_value") + '''"}})'''
        
        return userscenario_string  
    
    def send_user_scenario_string(self):
        """ 
         builds a user scenario and sends a RESTful message to the loadimpact server
         :return the response from the server
        """ 
        dict_data= self.parserClass.parse_and_build_jMeter_dict()
        user_scenario = client.create_user_scenario({
                                                     'name': "Vahid user scenario",
                                                     'load_script': self.build_user_scenario_string()
                                                     })
        return user_scenario
    
    def create_and_send_test_config(self):
        """
         builds a test configuration and sends a RESTful message to the loadimpact server
         :return the response from the server
        """
        dict_data= self.parserClass.parse_and_build_jMeter_dict()
        
        user_scenarios = client.list_user_scenarios()
        # we have uploaded only one user  scenario, so let's fetch its ID
        user_scenario_id = user_scenarios[0].id
        

        # This is just to test the REST API without using loadimpact's SDK
#         loadimpact_url = "https://api.loadimpact.com/v2/test-configs"
#         headers = {'Content-Type': 'application/json'}
#         payload = {
#                     'name': 'My test configuration',
#                     'url': "http://" + dict_data.get("domain") + "/",
#                     'config': {
#                                "load_schedule": [
#                                                  {
#                                                   "users": int(dict_data.get("VUs")), 
#                                                   "duration": int(dict_data.get("ramp_time"))
#                                                   }
#                                                  ],
#                                "tracks": [
#                                           {
#                                            "clips": [
#                                                      {
#                                                       "user_scenario_id": user_scenario_id, 
#                                                       "percent": 100
#                                                       }
#                                                      ],
#                                            "loadzone": LoadZone.AMAZON_IE_DUBLIN
#                                            }
#                                           ],
#                                "user_type": "vu"
#                                }
#                     }
        
#         response = requests.post(loadimpact_url, data=json.dumps(payload), headers=headers, auth=(api_token, ''))
#         print response.status_code
#         print response.json()

        
        
        config = client.create_test_config({
                                            'name': 'My test configuration',
                                            'url': "http://" + dict_data.get("domain") + "/",
                                            'config': {
                                                       "load_schedule": [
                                                                         {
                                                                          "users": int(dict_data.get("VUs")), 
                                                                          "duration": int(dict_data.get("ramp_time"))
                                                                          }
                                                                         ],
                                                       "tracks": [
                                                                  {
                                                                   "clips": [
                                                                             {
                                                                              "user_scenario_id": user_scenario_id, 
                                                                              "percent": 100
                                                                              }
                                                                             ],
                                                                   "loadzone": LoadZone.AMAZON_IE_DUBLIN
                                                                   }
                                                                  ],
                                                       "user_type": "vu"
                                                       }
                                            })

       
        return config
