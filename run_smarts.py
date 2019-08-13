from __future__ import absolute_import, division, print_function

import sys
import os.path
import argparse

import yaml

from smarts.runner import TestHandler
from smarts.env import Environment



def parse_config():
    home = os.path.expanduser('~')
    config = os.path.join(home, 'smarts.conf')
    if os.path.isfile(config):
        config = open(os.path.join(home, 'smarts.conf'))
        return yaml.safe_load(config)
    else:
        return None





description =\
""" """

epilog =\
""" """

command_help_string =\
"""[sub-command ...] commands passed to SMARTS. Sub-command includes:
- list (li)
    List the available tests or test suites
- print (p)
    Introspect a test-suite or an individual test-piece
- launch (r)
    Launch 1 or more test and/or test suites
"""

test_directory_string =\
"""Location of ITP's"""

env_help_string =\
"""The location of the environment.yaml file for the current machine"""

n_cpus_help_string =\
"""The number of CPU's to use for this run"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     add_help=False)

    command = parser.add_argument_group('Commands', 'Commands to issue to SMARTS')
    options = parser.add_argument_group('Options', 'Optional arguments for SMARTS')
    misc = parser.add_argument_group('Miscellaneous', 'Misc. options')

    command.add_argument('command',
                        nargs='*',
                        type=str,
                        default=None,
                        help=command_help_string)

    options.add_argument('--dir',
                        type=str,
                        default=None,
                        help=test_directory_string)
    options.add_argument('--env',
                        type=str,
                        default=None,
                        help=env_help_string)
    options.add_argument('-n',
                        '--cpus',
                        type=int,
                        default=None,
                        help=n_cpus_help_string)

    misc.add_argument('-h',
                      '--help',
                      action='store_true',
                      default=False,
                      help="Print this help statement")

    misc.add_argument('-u',
                      '--usage',
                      action='store_true',
                      default=False,
                      help="Print a usage statement")
    misc.add_argument('-v',
                      '--verbose',
                      type=int,
                      default=0,
                      help="Verbosity of debug print statments")

    args = parser.parse_args()

    command = args.command
    env     = args.env
    cpus    = args.cpus
    testDir = args.dir
    verbose = args.verbose

    if args.help:
        parser.print_help()
        sys.exit(-1)

    if args.usage:
        parser.print_usage()
        sys.exit(-1)

    if not command:
        print("ERROR: No command given to SMARTS. Use -h or --help to see a list of commands.")
        parser.print_usage()
        sys.exit(-1)
   
    """ Parse smarts.conf - Command-line options override smarts.conf """
    config = parse_config()
    if config and not env:
        env = config['Environment']

    if config and not testDir:
        testDir = config['Test Directory']
    
    if verbose > 0:
        print('DEBUG: Environment: ', env)
        print('DEBUG: Test Dir: ', testDir)

    """ Start the TestHandler and the Environment Class"""
    TestHandler = TestHandler(testDir)
    Environment = Environment(env)

    if verbose > 0:
        print('DEBUG: TestHandler Loaded Succsfully')
        print('DEBUG: Enviornment Loaded Succesfully')

    if verbose > 0:
        print("DEBUG: Command is: ", command)


    """ Parse command - And do the command """
    if command[0] == 'list' or command[0] == 'ls':

        if len(command) < 1:
            print("ERROR: list command takes at least two arguments. Use list help to see")
            print("ERROR: a full list of commands")
        elif command[1] == 'help': 
            print("List Help...")

        elif command[1] == 'tests' or command[1] =='t':
            TestHandler.list_tests()
            sys.exit(0)
        elif command[1] == 'suites' or command[1] == 's':
            TestHandler.list_suites()
        elif command[1] == 'modsets' or command[1] == 'm':
            Environment.list_modsets()
            sys.exit(0)
    elif command[0] == 'print' or command[1] == 'p':

        if len(command) < 1:
            print("ERROR: print command takes at least two arguments. Use print help to see")
            print("ERROR: a full list of commands")
        elif command[1] == 'help': 
            print("Print help message...")
        """ Print the tests that are within the specified suite """ 
        if command[1] == 'suite' or command[1] == 's':
            if len(command) > 3:
                for i in range(3, len(command)):
                    print('i:')
                    TestHandler.print_suite(command[i])

        """ Print the description of the specifiedtests """
        if command[1] == 'test' or command[1] == 't':
            if len(command) > 3:
                for i in range(3, len(command)):
                    print('i:')
                    TestHandler.print_test(command[i])

        """ Print the libraries/modules in specified modset"""
        if command[1] == 'modset' or command[1] == 'm':
            if len(command) > 3:
                for i in range(3, len(command)):
                    print('i:')
                    Enironment.print_modsets(command[i])

    elif command[0] == 'launch' or command[0] == 'l':
        if len(command) < 1:
            print("ERROR: print command takes at least two arguments. Use `launch help` to see")
            print("ERROR: a full list of commands")
        elif command[1] == 'help': 
            print("Launch help message...")

        """ Launch a list of tests and/or a list of suties """
        if len(command) > 2:
            TestHandler.launch(command)



