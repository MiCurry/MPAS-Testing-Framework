import os, sys, time

nprocs = 1
compatible_environments = ['kuusi','cheyenne']

def setup(tparams):

	return {'modset':'intel'}

def test(tparams, res):

	env = tparams['env']
	utils=env.get('utils')	

	res.set('completed', False)
	res.set('name', 'Build / Intel')

	if not env:
		print('No environment object passed to Build/Intel test, quitting')
		return res
	if not utils:
		print('No utils module in test environment, quitting Build/Intel test')
		return res

	if not env.contains_modset('intel'):
		res.set('err_msg', 'In Build/Intel test(), no modset for intel')
		return res

	e = env.mod_reset('intel', {})
	if e:
		res.set('err_msg', "In Build/Intel test(), error resetting to the modset 'intel'.")
		res.set('err_code', e)
		return res
	

	src_dir = tparams['src_dir']

	os.system('cp -R '+src_dir+'/src .')
	os.system('cp -R '+src_dir+'/Makefile .')

	#
	# First compile the init_atmosphere core
	#
	os.system('time make ifort CORE=init_atmosphere > make.init.log 2>&1')
	if not os.path.isfile('init_atmosphere_model') or not os.path.getsize('init_atmosphere_model') > 1000000:
		res.set('err_msg', 'Intel build test failed to compile init_atmosphere_model')
		res.set('err_code', 1)
		res.set('success', False)
		res.set('completed', True)
		return

	#
	# Then clean and compile the atmosphere core
	#
	os.system('make clean CORE=atmosphere > clean.log 2>&1')
	os.system('time make ifort CORE=atmosphere > make.model.log 2>&1')
	if os.path.isfile('atmosphere_model') and os.path.getsize('atmosphere_model') > 1000000:
		res.set('err_msg', 'Intel build test passed')
		res.set('err_code', 0)
		res.set('success', True)
	else:
		res.set('err_msg', 'Intel build test failed to compile atmosphere_model')
		res.set('err_code', 1)
		res.set('success', False)


	res.set('completed', True)
	
	return
