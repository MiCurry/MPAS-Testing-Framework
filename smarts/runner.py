from __future__ import absolute_import, division, print_function

import sys
import os, os.path

import yaml

class TestHandler:

    def __init__(self, testDir):
        """ Initialization function for the TestHandler class.  """
        
        # Find and open the test directory and generate a list of ITP's

        # Read the test_suites.yaml file in the test directory and 
        # generate a list of suites and the ITP's that are associated with
        # each suite

        if not os.path.isdir(testDir):
            print("ERROR: The given test directory (", testDir, ") was not found")
            print("ERROR: Please insurance the correct directory was given")
            print("ERROR: or specify a new directory with --dir")
            sys.exit(-1)
        else:
            self.testDir = testDir

        self.load_available_tests(self.testDir)

        if os.path.isfile(os.path.join(testDir, 'test_suites.yaml')):
            pass
            #print("test_suites.yaml loaded successfully!")
            #self.load_test_suites(os.path.join(testDir, 'test_suites.yaml'))
           

        else: # No suite file found
            print("No test_suites.yaml file found within ", testDir)
            self.suites = None
    

    def load_test_suites(self, suiteFile):
        """ Load and store each test suite and each suite's associated ITPs """
        suites = yaml.safe_load(suiteFile)
        print("Load test suites called, but no suites loaded - not implemented")
        return

    def load_available_tests(self, directory):
        """ Find and list all the available tests in the test directory """
        self.availTests = []

        for test in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, test)):
                self.availTests.append(test)

    def list_tests(self):
        print("Tests in ", self.testDir, ":", sep='')
        for test in self.availTests:
            print(test)

    def list_suites(self):
        """ Read and list all the available tests suites in the test directory """
        # Print the tests.yaml name, location and the test suites available
        pass

    def launch(self, command):
        """ Launch a 1 or more tests or 1 or more suites or a combination of
            both tests and suites """

        pass
