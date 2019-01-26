import os, sys, time

nprocs = 1
compatible_environments = ['kuusi','cheyenne', 'snorri']

def setup(tparams):

	return {'modset':'gnu'}

def test(tparams, res):

	env = tparams['env']
	utils=env.get('utils')	

	res.set('completed', False)
	res.set('name', 'Build / GNU')

	if not env:
		print('No environment object passed to Build/GNU test, quitting')
		return res
	if not utils:
		print('No utils module in test environment, quitting Build/GNU test')
		return res

	if not env.contains_modset('gnu'):
		res.set('err_msg', 'In Build/GNU test(), no modset for gnu')
		return res

	e = env.mod_reset('gnu', {})
	if e:
		res.set('err_msg', "In Build/GNU test(), error resetting to the modset 'gnu'.")
		res.set('err_code', e)
		return res
	

	src_dir = tparams['src_dir']

	os.system('cp -R '+src_dir+'/src .')
	os.system('cp -R '+src_dir+'/Makefile .')

	#
	# First compile the init_atmosphere core
	#
	os.system('make clean CORE=atmosphere >& /dev/null')
	os.system('make clean CORE=init_atmosphere PRECISION=single >& /dev/null')
	print("Compiling init_atmosphere with gfortran...")
	os.system('time make gfortran CORE=init_atmosphere PRECISION=single > make.init.log 2>&1')
	if    not os.path.isfile('init_atmosphere_model') 
	   or not os.path.getsize('init_atmosphere_model') > 1000000:
		res.set('err_msg', 'GNU build test failed to compile init_atmosphere_model')
		res.set('err_code', 1)
		res.set('success', False)
		res.set('completed', True)
		return

	print("init_atmosphere built with gfortran!\n")

	#
	# Then clean and compile the atmosphere core
	#
	os.system('make clean CORE=atmosphere >& /dev/null')
	os.system('make clean CORE=init_atmosphere >& /dev/null')

	print("Compiling atmosphere model with gfortran...")
	os.system('time make gfortran CORE=atmosphere PRECISION=single')
	print("Compiling atmosphere model again with gfortran to get past errors") 
	os.system('time make gfortran CORE=atmosphere PRECISION=single')
	if os.path.isfile('atmosphere_model') and os.path.getsize('atmosphere_model') > 1000000:
		res.set('err_msg', 'GNU build test passed')
		res.set('err_code', 0)
		res.set('success', True)
		print("Built atmosphere model with gfortran!\n")
	else:
		res.set('err_msg', 'GNU build test failed to compile atmosphere_model')
		res.set('err_code', 1)
		res.set('success', False)


	res.set('completed', True)
	
	return
