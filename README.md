test-builder
============
Converting JMeter to Load Impact: A Loading Test builder based on the Load Impact Python SDK


Introduction
=============
This application implements the idea of building the load test configurations automatically.
To fulfill its mission, it carries out several steps:

1. It fetches the JMX files from a drop location (assests in the root of the project),
   and parse the relevant fields. Right now we have only one JMX file, but the system can be
   easily adjusted to  iterate over the drop location and parse then later. 
   Another idea is to sort(by time, etc) and possibly delete the JMX files IF we don't need
   to keep them.

2. While parsing JMX files, it builds a python dictionary from the interested values 
   to be used later.
   
3. Next, it builds a lua-syntax-friendly string as a string representation 
   of user scenario.
   
4. Using the loadimpact's RESTful SDK, it sends the user scenario to their servers and
   gets the response back from the server.
   
5. Finally it creates a load test configuration and sends it to the server 
   by, again, loadimpact's RESTful SDK.
   To test the performance of SDK, another RESTful message has been created with 
   Requests library and has been marked as a comment in the source code.               

6. This application has a good degree of test coverage. **Test Driven Development** was the
   the major approach while building the application. 
   
   

Installing
==========
To run the application properly, you should install two libraries :
```bash
$ pip install loadimpact
$ pip install requests
```
After installing the necessary libraries, clone the project into your local machine


CLI interface
==============
A `manage.py` file has been built to behave as a command line interface for 
the application. 
To see the options that it provides, issue the following command:
```bash
$ python manage.py -h
```
As you can see there are three options : `help` , `test` and `run` the application 


First create an API Token
=========================
Please Go to loadimpact.com account page and create an API Token.
Then `export` the Token as an `environment variable	`. 
```bash
$ export LOADIMPACT_API_TOKEN=YOUR_API_TOKEN_GOES_HERE
```

Second run the tests
====================
Let's test the application first
```bash
$ python manage.py -t test
```
here is a response 
```bash
test_version (test_utils.TestUtilsModuleFunctions) ... ok
test_fetch_filename (test_main.TestJMXParse) ... ok
test_if_Jmetertestplan_exists (test_main.TestJMXParse) ... ok
test_if_assets_folder_exits (test_main.TestJMXParse) ... ok
test_parse_and_build_jMeter_dict (test_main.TestJMXParse) ... ok
test_build_user_scenario_string (test_main.TestUserScenarioCreator) ... ok
test_send_user_scenario_string (test_main.TestUserScenarioCreator) ... ok

----------------------------------------------------------------------
Ran 7 tests in 4.692s

OK
```


Third run the application
=========================
To run the application, type the following command
```bash
$ python manage.py -r run
```
A successful running should be 
```bash
Building the load configuration test and uploading to loadimpact servers.
.........................................
Configuration test uploaded successfully !
```


