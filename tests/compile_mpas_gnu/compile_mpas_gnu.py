



description = {
    'Long Name'         : 'Compile MPAS - GNU',
    'Short Name'        : 'compile_mpas_gnu',
    'Description'       : 'Compile mpas with the GNU compile',
    'CPUs'              : 4,
    'Test Dependencies' : None,
}

def init_test(env):
    """ 
    * Load the modeset / setup the enviornment
    * Make sure the modest and the enviornment has correctly been setup
        - i.e. Insure that the required libaries exsist, and if they don't
        prompt the user that they do not.
    """
    env.load_modset('gnu-9.1.0')


    pass

def run_test():
    pass

def finialize_test():
    pass

