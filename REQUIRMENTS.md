# MPAS-Testing-Framework

The Simple-MPAS-Regression-Testing-Framework (SMARTS).

# Requirements

**General**

1. SMARTS should be ran as a command line utility (i.e. so it can be ran
everywhere), thus it should be able to install via pip OR simply added to the
PATH environment variable.

2. SMARTS should consist of two main components - One that controls the
execution of tests (the driver) and provide tools for writing tests
(tests/operants).

3. Users will be able to write, launch, check and report the result of tests
using Python to check the results of the tests or manipulate the results of the
test (i.e.  make a plot or write a report)

4. Tests can be simple (creating a file on a machine) to complicated (running an
ensemble simulation)

5. SMARTS will be able to launch any type of application specifically: C, C++,
Fortran, Python, or any type of operating system programs, scripts or
processes.

6. SMARTS will be Portable - SMARTS must work on a variety of environments and
machines including desktops, HPCs and cloud resources (???). SMARTS should be
implemented in Python 3.x and have support for Python 2.7.

7. SMARTS should be aware of the amount of resources (CPU, memory, disk space,
compilers, libraries/modules, HPC queue system) of the system.

8. A file should describe the resources of the system (that are described
above) in a file format that is both human and computer readable (i.e. XML,
JSON, or YAML).

9. Tests can be ran with 1 or more processes

10. Tests can be collected into "test suites" which is a way to describe a bulk
of tests to be run as a single command.

11. Tests can be organized into a hierarchy where some tests are dependent upon
another (or others) and won't run unless a dependent test completes
successfully (for instance running a simulation if and only if the code
compiles)

12. Each test will contain a description of itself. The description includes
needed modules and environment variables, the number of CPU's it requests to
run with, or its requested allocation for an HPC (i.e. queue, number of nodes,
number of CPU's, runtime etc.). 

13. SMARTS will be able to run with or without a schedule (such as PBS). If no
schedule is present SMARTS will schedule (in the order that the tests are
given) upon the number of processes it is allowed to run with.

14. SMARTS should be able to run multiple tests at the same time depending upon
the amount of CPU's each test requires and the amount of CPU's that are
available at the current time

15. Each run of SMARTS should create a directory of the current date and time,
and within that directory create directories of each individual test piece.

16. The SMARTS system should use a Standard Library, which is a directory that
contains assets that are repeatedly used. I.E. meshes, static files,
initialization files, GFS data etc.

17. The environment file should describe the location of compilers and libraries
as well as the location of the standard library. 

18. SMARTS should be able to load compilers and libraries on the system that are
specified by a PATH or that can be loaded
via the `lmod` (`module`) command.

19. Module (`lmod`) module names and version and compilers and library's name,
location and version should both be listed in the environment file. 

20. Compilers and libraries can be loaded into different 'modsets', which is a
collection of a compiler and libraries that are compiled with that compiler.

21. SMARTS will not run jobs that are too big for the environment (i.e. if a job
asks for more CPU's then is allowed on the current machine.)

22. The SMARTS should report on its current operating status. When it starts,
what tests it will run, what test is running, and when tests finish and will
write its status to a stdout which can be redirected to a file if desired.

23. A requirements.txt file should be used to handle all the necessary
dependences of SMARTS.

**Documentation**

24. SMARTS should be well documented, both the test launcher and how to create
operants. Specifically, the interaction between the two should be described.

25. SMARTS documentation should be simple and clear, and look to educate users on
how the system is structure and how the system works. The documentation should
also contain references for all functions (especially functions that act as
utilities to creating tests).

26. The test launcher needs to be simple and intuitive for external users to
understand and contribute code.

27. Errors encountered by the test launcher should produce error messages that
are clear to the user what went wrong and what they need to do to correct it.

**Reporting**

28. Operants should be able to report their results in a variety of different
ways depending on the user's test requirements. Results can be reported to
stdout, a log file, plots, a TeX document, email (for future) or a combination
of them all.
