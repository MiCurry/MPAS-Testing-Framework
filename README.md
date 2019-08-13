# MPAS-Testing-Framework
This is a regression testing suite being implemented in python for MPAS, the
Model for Prediction Across Scales, which is a part of the MMM division at
NCAR.

# Usage

## CRC
```
Name: Environment
Responsibilities:
    * Retrieve and store information about the current environment
    * Schedule tests depending on the number of CPU's of the CPU and the
      requested number by each test
    * Launch tests on the machine by using the correct machine-dependent
      launcher - i.e. an HPC scheduling system, or a normal mpi launch.
    * Load/link the required libraries for running the specified test
Collaborators:
```

```
Name: Test - Test Runner - Test Handler
Responsibilities:
    * Keep track of the current status of a single test, whether scheduled,
      running, stopped, finished or failed.
    * Stop, start, abort, or remove tests that are scheduled to run, or that
      are currently running.
    * Issue commands for creating any output that will be used to report the
      result of a test
    * Communicate the status of tests to and from the user in some method -
      (Output, but also maybe a shell to issue commands? or a deamon?)
    * Handle errors that are not caught by the Test Description (i.e. runtime
      errors or terminating signals).
    * Report any non-kill signals
Collaborators:
```

```
Name: **Operant**
Responsibilities:
    * Describe the needed requirements to run a test
        - Number of CPUS
        - Type of execution (MPI/normal)
        - Needed library dependencies
    * Contain logic to setup, run a single or multiple tests
    * Contain logic to determine if a test has passed or has failed (if needed)
    * User defined - users should be able to write scripts, functions, programs
    to meet their desires.
Collaborators:
    * Environment
    * Test Runner
    * Reporter
```

```
Name: Reporter
Responsibilities:
    * Generate simple reports as defined by the user in an Operant in the form
    of standard output, logs, or TeK documents.
    * Act as a wrapper for the user. Easily writes reports with a few system
    calls and easily include common assets such as plots, logs, files etc.
Collaborators:
    * Environment - To report on what environment was used
    * Operant
```

# Resources/Links
* [PEP 8 - Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
* [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
