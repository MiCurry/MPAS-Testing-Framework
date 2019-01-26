#
# MPAS Regression Testing Framework
#

# test_driver.py


#
#
# Import all necessary modules
#
#
from __future__ import print_function
import os, sys
import datetime
import argparse

import xml.etree.ElementTree as ET

import importlib as ilib
import pkgutil

import threading
from distutils import spawn
import multiprocessing

from utils.testProcess import ResultManager
from utils.testProcess import testProcess


parser = argparse.ArgumentParser(
		description=("\n\n************** MPAS Regression Testing Framework **************\n\n"
                    "This testing framework runs selected tests from a suite. A folder called\n"
                    "regtest.$TIMESTAMP$ will be made in this directory with test files/results."), 
			epilog=("For more information, visit the repository on Github and read the README.\n"
					"https://github.com/daniel-j-henderson/MPAS-Testing-Framework\n\n"
					"***************************************************************"), 
   formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument(
		  'names', 
		nargs='+',	
        help=("The test/group names; that is, the names of every test \n" 
        	 "or test group (see Tests.xml) you'd like to run. Required"))

parser.add_argument('-n', 
                    type=int, 
                    metavar='NPROCS', 
                    help=("The maximum number of processors to be used at any\n"
                         "given time during testing"))

parser.add_argument('-env', 
                    metavar="Environmnent", 
                    help=("Explicit name/path of the XML file that defines the testing\n"
                         "environmnt, like an Environment.xml, yellowstone.xml, etc. \n"
                         "Default: 'Environment.xml'"))

parser.add_argument('-src', 
                    metavar="MPAS_SRC_DIR",
                    help=("The relative path to the directory containing the MPAS code\n"
                         "to be tested. This is the directory that will be\n"
                         "compiled/executables will be gathered from. If not specified,\n"
                         "the test_driver.py must be launched from within the source\n"
                         "code directory.\n"
                         "Default: present working directory"))

args = vars(parser.parse_args())

utils = ilib.import_module('utils.utils')



#
#
# Check for any necessary executables
#
#

if not spawn.find_executable('pdflatex'):
	print("The executable 'pdflatex' could not be found, so a pdf report of test results cannot be made. "
          "If you would like to see a basic results printout on the screen, or generate the '.tex.' file "
          "for reference/future use, continue. Would you like to continue?")
	choice = raw_input('y/n: ')
	if choice in ['n', 'N', 'no', 'NO']:
		os._exit(4)


#
#
# Set up the environment object
#
#
timestamp = datetime.datetime.now().replace(microsecond=0).isoformat().replace('T', '_').replace(':', '.')
fnames = os.listdir('.')
config_file = None
cmdargs = sys.argv[:]

if args['env']:
	config_file = args['env']
elif 'Environment.xml' in fnames:
	config_file = 'Environment.xml'
else:
	print('Please provide an environment configuration file in xml form.')
	os._exit(1)

# TODO: What is the following code block doing?
env = utils.Environment() # TODO: Comment, what is happening? - What is Utils?
root = ET.parse(config_file).getroot()
filepath = root.get('path')
env.set('name', root.get('name'))
env.set('pathSL', root.get('pathSL'))
env.set('modules', root.get('modules'))

# TODO: What is happening here?
if env.get('modules'):
	env.set('LMOD_CMD', root.get('LMOD_CMD'))
for modset in root.findall('modset'):
	env.add_modset(modset.get('name'), modset)
	if modset.get('default') in ['true', 'True', 'TRUE']:
		env.set('default_build_env', modset.get('name'))
		env.set('default_build_target', modset.get('compiler'))
if not env.get('default_build_env'):
	env.set('default_build_env', 'intel')
	env.set('default_build_target', 'ifort')
if not env.contains_modset('base'):
	print('Environment XML file must contain base modset.')
	os._exit(1)	
if root.get('PYTHONPATH'):
	os.environ['PYTHONPATH'] = root.get('PYTHONPATH')
	sys.path.append(root.get('PYTHONPATH'))
env.mod_reset('base')

# Depending on the batch system, put the necessary options (things like
# project codes or queue names) in the environment object in a dict
if root.get('type') == 'LSF':
	env.set('type', utils.Environment.ENVLSF)
	options = {}
	for lsf_option in root.findall('lsf_option'):
		options[lsf_option.get('name')] = lsf_option.get('value')
	env.set('lsf_options', options)
elif root.get('type') == 'PBS':
	env.set('type', utils.Environment.ENVPBS)
	options = {}
	for pbs_option in root.findall('pbs_option'):
		options[pbs_option.get('name')] = pbs_option.get('value')
	env.set('pbs_options', options)
else:
	env.set('type', utils.Environment.NONE)
	
# Set the total number of cores avaliable
# Either specified by the env folder or by the user
if root.get('max_cores'): # TODO: No Default?
	total_procs = int(root.get('max_cores'))
if args['n']:
	total_procs = args['n']

print('Max Cores: '+str(total_procs))

# TODO: Why are we doing this here? What if something doesn't want to use
# netcdf4?
if pkgutil.find_loader('netCDF4'):
	nc = ilib.import_module('netCDF4')
	print("Found netCDF module")
else:
	nc = None
# TODO: Ditto with numpy
if pkgutil.find_loader('numpy'):
	np = ilib.import_module('numpy')
	print("Found numpy module")
else:
	np = None

# TODO: Likewise for here, why are wet setting these as env when we want the
# test runner to be as bare as possible? We only want these if we are going to
# run them via a test
env.set('utils', utils)
env.set('nc', nc)
env.set('np', np)

# Set the source directory - or use the current one
# TODO: Possibly an output message here:
# "Setting the source directoy to `src`"
# "Using the current directory - specifcy a directory with -src"
if args['src']:
	src_dir = args['src']
else:
	src_dir = os.getcwd()

pwd = os.getcwd() # TODO: Seems out of order
SMARTS_dir = os.path.dirname(os.path.realpath( __file__ )) # TODO: Ditto


# TODO: We have a 'root' above, so this is confusing without a comment. I think
# we are getting the avaliable tests from the Test.xml file?
tests = {}
root = ET.parse(SMARTS_dir+'/Tests.xml').getroot()
for el in root:
	if el.tag == 'test_group' and el.get('name') in args['names']:
		group_name = el.get('name')
		tests[group_name] = []
		for t in el:
			tests[group_name].append(t.get('name'))
for key in tests:
	if key in args['names']:
		args['names'].remove(key)

if len(cmdargs) > 1:
	tests['misc'] = []
	for i in range(len(args['names'])):
		tests['misc'].append(args['names'][i])



results = []
tparams_base = {'src_dir':src_dir, 'SMARTS_dir':SMARTS_dir, 'env':env}

container = pwd+'/'+'regtest.'+timestamp
os.system('mkdir '+container)



#
#
# Make a process for each test
#
#
unfinished_tests = []
managers = {}

for group_name, test_arr in tests.items():
	for subdir in test_arr:
		
		try:
			sys.path.append(SMARTS_dir+'/'+subdir)
			mod = ilib.import_module(subdir)
		except ImportError:
			print("'"+subdir+"' is not a test module, skipping it")
			continue

		try: # TODO: Line below should be split
			if (env.get('name') not in mod.compatible_environments 
			          and 'all' not in mod.compatible_environments):
				print('The '+subdir+' test is not compatible with this environment ('+env.get('name')+')')
				print('-- If it is compatible, please add it the'
					  'compatible_environments list in', subdir, '/', subdir, '.py')
				continue
		except AttributeError:
			pass

		test_dir = container+'/'+subdir
		if mod.nprocs > total_procs:
			print('Cannot perform '+subdir+' test due to resource constraints')
			continue	

		managers[subdir] = ResultManager()
		managers[subdir].start()
		r = managers[subdir].Result()
		#TODO: Line too long
		unfinished_tests.append(testProcess(func=mod.test, setup=mod.setup, nprocs=mod.nprocs, initpath=test_dir, name=subdir, result=r, group=group_name))
		try:
			unfinished_tests[-1].dependencies = mod.dependencies
		except AttributeError:
			pass


#
#
# Start tests, keeping the number of cores in use below the max
#
#

procs_in_use = 0
tests_in_progress = []
finished_tests = []
unfinished_tests.sort(key=lambda t: t.get_num_procs(), reverse=True)
while unfinished_tests:
# I think the one below it is waiting for the procs to finish, but I'm
	for t in tests_in_progress: # Loop through each of the steps
		if not t.is_alive(): 
			# If the test is dead decrement then number of procs being ran
			procs_in_use -= t.get_num_procs()
			finished_tests.append(t)
			tests_in_progress.remove(t)
	if procs_in_use < total_procs: 
		# If we have an open proc, then start a new test proc?
		for t in unfinished_tests: # Loop through unifnished tests ... okay :)
			# TODO: I think this try execpt could me more explicit
			# TODO: Also what is happening?
			try:
				# TODO: What what what is happening in this try block ???
				depends = t.dependencies
				if len(finished_tests) > 0: 
					finished = [test.get_name() for test in finished_tests]
				else:
					finished = []
				if len(unfinished_tests) > 0:
					unfinished = [test.get_name() for test in unfinished_tests]
				else:
					unfinished = []
				if len(tests_in_progress) > 0:
					inprogress = [test.get_name() for test in tests_in_progress]
				else:
					inprogress = []
				ready = True
				# TODO: This is waaaaayyy too deep
				for dep in depends:
					if dep not in finished:
						if dep not in unfinished and dep not in inprogress:
							print('Test '+t.get_name()+' depends on a test which we are not testing, so it will be skipped.')
							unfinished_tests.remove(t)
						ready = False
						continue
				if not ready:
					continue
			# TODO: What part of the cod will throw an
			# attribute error?
			except AttributeError: 
				pass
			# TODO: What is this?
			# What is t? t == tests??
			if t.get_num_procs() <= total_procs - procs_in_use:
				procs_in_use += t.get_num_procs()
				tests_in_progress.append(t)
				unfinished_tests.remove(t)
				tname = tests_in_progress[-1].get_name()
				print('\nStarting '+tname+' test.')


				test_dir = container+'/'+tname
				os.system('mkdir '+test_dir)
				tparams = tparams_base.copy()
				tparams['test_dir'] = test_dir


				popdir = os.getcwd()
				os.chdir(test_dir)
				prec = t.setup(tparams)
				os.chdir(popdir)

				if 'modset' in prec:
					if env.contains_modset(prec['modset']):
						env.mod_reset(prec['modset'])

				if 'exename' in prec:
					exenames = prec['exename']
					if type(exenames) != type([]):
						exenames = [exenames]
					for exename in exenames:
						if not os.path.exists(src_dir+'/'+exename):
							env.mod_reset(env.get('default_build_env'))
							e = utils.compile(src_dir, exename.replace('_model', ''), env.get('default_build_target'))
							if e:
								r = utils.compile(src_dir, exename.replace('_model', ''), env.get('default_build_target'), clean=True)
								if r:
									print(exename+' does not exist in '+src_dir+' and cannot be built')
									os._exit(1)
						os.system('cp '+src_dir+'/'+exename+' '+test_dir)	

				if 'files' in prec:
					files = prec['files']
					if 'locations' in prec:
						locations = prec['locations']
					else:
						locations = [test_dir]*len(files)
					found_files=[False]*len(files)
					for i in range(len(files)):
						if utils.retrieveFileFromSL(files[i], locations[i], env):
							found_files[i] = True
					tparams['found_files'] = found_files
					tparams['files'] = files

				t.tparams = tparams
				tests_in_progress[-1].start()
# TODO: This can probably(?) be combined with the while loop of the same name
# Above
while tests_in_progress:
	t = tests_in_progress[0]
	t.join()
	finished_tests.append(t)
	tests_in_progress.remove(t)

finished_tests.sort(key=lambda t: t.get_group())
for t in finished_tests:
	results.append((t.get_result()._getvalue(), t.get_group()))
	managers[t.get_name()].shutdown()

# 
# 
# Report Results
#
#
result_dir = container+'/results'
os.system('mkdir '+result_dir)

tfname = 'Results.'+timestamp+'.tex'
popdir = os.getcwd()
os.chdir(result_dir)
f = open(tfname, 'w')
utils.writeReportTex(f, results)
f.close()
if spawn.find_executable('pdflatex'):
	os.system('pdflatex -halt-on-error -interaction=batchmode '+tfname)
	os.system('rm *.aux *.log *.tex')
os.chdir(popdir)


for t in results:
	r = t[0]
	if(not r.get('completed')):
		print('Test did not complete.')

	print(r.get('name')+' test ' + ('succeeded' if r.get('success') else 'failed'))

	if r.get('err_code') is not None:
		print ('   with error code '+str(r.get('err_code')))

	if r.get('success') == False:
		err = r.get('err')

		if type(err) == list:
			print('List of items in error:')
			for e in err:
				print('    '+str(e))
		elif type(err) == str:
			print(err)

print ('Done.')

