import os, sys

# 'nprocs': max number of MPI tasks this test may use at any given time.
# 'compatible_environments': list of environments this test can run on. Optional. default: all.
# 'dependencies': list, the names of any specific tests which must be performed before this test.
nprocs = 36
compatible_environments = ['all']
dependencies = ['compile_intel']

def setup(tparams):
    # return the name of the executable you want (it will be linked into your
    # testing sandbox) and the max number of processors your test will use at a
    # given time. Also, return a list of the files you want from the Standard 
    # Library, and they will be put in your test_dir.

    # setup() is run in your test sandbox directory, so you can make any
    # changes to it that you need. Note: setup is not necessarily run directly
    # before test(), so it is unwise to make any changes that might be reverted
    # by some other test before the test() function is called

    files = ['x1.2562.grid.nc', 'x1.2562.graph.info.part.36'] #list of desired files from the SL
    return {'files':files, 'exename':'terrain_model'}

    """
    Return Items (in a dictionary)
    'files': list of desired files from SL. 
    'locations': list of paths in which to place those files.
    'exename': name of executable the test would like to use (will be linked
               into the testing sandbox).
    """

def test(tparams, res):
    # Arguments: tparams, a dictionary of useful things (like the environment
    # object
    # and various directory paths) and res, the result object for the test. Res
    # is already initialized.
    
    """
    tparams =  {'src_dir':top-level MPAS directory path, 
                    'SMARTS_dir':path to SMARTS directory, 
                    'env':environment object, 
                    'test_dir':path to testing sandbox (absolute), 
                    'found':[True, False, ..., True] list of logicals that
                    corresponds to each file requested in the setup() method
                    and whether that file was found in the SL
                    }
                    type: dictionary

    res = Result() 
                    res.set('key', value) :: sets a result value
                    res.get('key')           :: gets a result value
        
                    type: Result object
        
                    You must set the key 'completed' before returning. You
                    should also set the keys 'name', 'success', 'err_code',
                    'err_msg', etc. as you see fit. The driver will look for
                    common keys, but it will also try and discover your keys
                    and report them as best it can.
    """

    env = tparams['env']
    utils=env.get('utils')

    # The res object must have the 'completed'
    # attribute set upon return.
    res.set('completed', False)
    res.set('name', 'terrain_core_test')

    if not env:
        print('No environment object passed to Example test, quitting')
        return res
    if not utils:
        print('No utils module in test environment, quitting Example test')
        return res
    
    test_dir = tparams['test_dir'] # file path of testing sandbox, absolute
    my_dir = tparams['SMARTS_dir']+'/terrain_core_test' # store any small files you need, e.g. namelists, in here somewhere

    utils.linkAllFiles(my_dir+'/inputs', './')

    pbs_options = { '-A':'NMMM0013',
                   '-l':'walltime=00:10:00',
                   '-q':'regular' }

    myRun = utils.modelRun(test_dir, 
                           'terrain_model', 
                           nprocs, 
                           env, 
                           add_pbsoptions=pbs_options)
    print('Starting model run')
    e = myRun.runModelBlocking() # As an example, sets the result as if a
                                          # successful model run occured
    myRun.terminate()
    print('Finished model run')

    e = myRun.get_result()

    res.set('success', e.get('completed') and e.get('success')) 
    res.set('err_code', e.get('err_code'))
    res.set('err_msg', 'Example test ran fine')
    res.set('completed', True)
    
    return
