# Percepto

The goal of this assignment is to write a Python script that automates tasks on Bestbuy website, covering UI testing
using Selenium.

This solution has a test file - test_best_buy.py - under src.tests, which contains several tests' scenarious.
The project's source reside under src folder.

The web client resides under src.clients folder.
Selenium driver should be created automatically on the first run and will be placed under src.drivers folder.

Tests are running under the pytest work frame.
it has a conftest.py file which initiate the client as well as calls for tearDown at its end.

Tests' global (common) args and other are placed under src.cfg.cfg_global at settings.py .
Args per a specific test, resides under src.cfg.cfg_tests, and are named by the test name itself.
"conftest.py" calls these file and load the data, which the tests utilize afterwords.

## About the client;
it resides under src.clients (web_client.py).
There are several other clients, which support the entire logic.
The  base_elements.py is more important than the other and support the web client with some additional logic, which helps
to find the elements, to wait for elements, to wrap calls coming from the client and to add them an additional functionality.
The client uses a wrapper - called "alerts_handling" (which resides in the base_elements.py) and which functions as an 
alerts/popus mitigatgor as well.

## Before running the tests:
  - Create a Python virtual environment and activate it (instruction can be found later in the text below)
  - upgrade the pip package by: **python -m pip install --upgrade pip**
  - install setup.py by: **python setup.py install** (include the dot at the end) - see elaboration below.
  - install the requirements.py by:  **pip install --upgrade -r requirements.txt**

## To run the tests via pytest (for both Windows and Linux)
- First, install the setup.py as mentioned above 
- To run the test via cli, while being in the **project's root tree**, type (and virtualenv is activated):

  ** python -m pytest ./src **


## Log files
Are written to the logs folder which is under the tree root.

