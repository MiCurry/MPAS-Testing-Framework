import os, sys

class Result:
	
	def __init__(self):
		self.attributes = {}

	def get(self, attname):
		return self.attributes[attname]

	def set(self, attname, value):
		self.attributes[attname] = value
		return

class Environment:
	params = {}

	def get(self, pname):
		return self.params[pname]
	def set(self, pname, value):
		self.params[pname] = value
		return

def runModel(dir, n, env):

	if env.get('name') != 'mmm':
		print('Trying to run model in '+env.get('name')+' environment which is not yet supported')
		return False

	if (not os.path.isdir(dir)):
		print('Invalid directory supplied to runModel: ' + dir)
		return False
	popdir = os.getcwd()
	os.chdir(dir)
	
	cmd = 'mpirun -n '+str(n)+' ./atmosphere_model'
	print(cmd)
	err = os.system(cmd)
	if (err):
		print('error running mpas in '+dir+', error code '+str(err))
		os.chdir(popdir)
		return False
	os.chdir(popdir)
	return True


def compareFiles(a, b, env):
	nc = env.get('nc')
	np = env.get('np')
	if not nc:
		print('In utils module, netcdf module not provided in environment object')
		return -1
	if not nc:
		print('In utils module, numpy module not provided in environment object')
		return -1

	r = Result()
	r.attributes['diff_fields'] = []
	r.attributes['num_diffs'] = []

	f1 = nc.Dataset(a, 'a')
	f2 = nc.Dataset(b, 'r')

	for k in f1.variables.keys():
		if k not in f2.variables:
			print('compareFiles: Element '+k+' is in '+f1+' but not '+f2)
			continue
		if not np.array_equal(f1.variables[k][:], f2.variables[k][:]):
			r.attributes['diff_fields'].append(k)
			i = 0
			n = 0
			for i in range(0, len(f1.variables[k][:])):
				if f1.variables[k][i] != f2.variables[k][i]:
					n += 1
			r.attributes['num_diffs'].append(n)
	f1.close()
	f2.close()
	return r


def searchForFile(tag, name, relpath):
	import xml.etree.ElementTree as ET
	for child in tag:
		if child.tag == 'file':
			if child.get('name') == name:
				relpath.append(name)
				return True
	for child in tag:
		if child.tag == 'subdir':
			if searchForFile(child, name, relpath):
				relpath.append(child.get('subpath'))
				return True
	return False

# def retrieveFileFromWebSL(name, dest, env):
# 	import xml.etree.ElementTree as ET

# 	# temp_dir = '__temp__/'
# 	# os.system('mkdir '+temp_dir)
# 	#env.pathWebSL = 'www2.mmm.ucar.edu/.../Standard-Library/'
# 	#download Library.xml to temp
# 	#parse 

# 	# name_zipped = name+'.tar.gz'
# 	# repath = []
# 	# found = searchForFile(root, name_zipped, relpath)

# 	# download file
# 	# unzip if necessary
# 	# move to correct spot
# 	# remove temp folder
# 	return 0


def retrieveFileFromSL(name, dest, env):
	import xml.etree.ElementTree as ET

	if env.get('name') == 'Yellowstone':
		print('On yellowstone, looking for '+name)
	elif env.get('name') == 'mmm':
		print('On an MMM machine, looking for '+name)
	else:
		print('Unknown environment.')
	popdir = os.getcwd()
	if env.get('pathSL'):
		os.chdir(env.get('pathSL'))
	else:
		print('No SL in this environment')
		return False

	#TODO check for existence
	root = ET.parse('Library.xml').getroot()
	filepath = root.get('path')
	relpath = []
	
	found = searchForFile(root, name, relpath)
	if found:
		for subpath in reversed(relpath):
			filepath += subpath
		print('file found: '+filepath)
		os.system('ln -sf '+filepath+' '+dest)
	else:
		print("didn't find the item")
	os.chdir(popdir)
	return found

def linkAllFiles(dirA, dirB):
	for file in os.listdir(dirA):
		if (file[0] == '.'):
			print(file)
			continue
		if file in os.listdir(dirB):
			print('replacing '+dirB+'/'+file)
			os.system('rm '+dirB+'/'+file)
		os.system('ln -s '+dirA+'/'+file +' '+ dirB+'/'+file)


def translate(string):
	str = ''
	if type(string) != type(str):
		return ''

	return string.replace('_', '\\_')

	
def writeReportTex(f, results):

	preamble = '\\documentclass[a4paper]{article} \n\\usepackage[english]{babel} \n\\usepackage[utf8x]{inputenc} \n\\usepackage{graphicx}\n\\usepackage[T1]{fontenc} \n\\usepackage[a4paper,top=3cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry} \n\\usepackage[colorinlistoftodos]{todonotes} \n\\title{MPAS Testing Framework Test Results} \n\\begin{document} \n\\maketitle'
	f.write(preamble)
	f.write('\n')
	f.write('\\section{Successful Tests}\n')
	for r in results:
		print(r.attributes)
		if not r.get('success'):
			continue
		f.write('\\subsection{'+r.get('name')+'}\n')
		f.write('\\begin{tabular}{|p{.3\\textwidth-2\\tabcolsep} |p{.7\\textwidth-2\\tabcolsep} |} \\hline\n')
		for k, v in r.attributes.items():
			f.write(translate(str(k)) + ' & ' + translate(str(v)) + ' \\\\ \\hline \n')
		f.write('\\end{tabular}\n')
	f.write('\\section{Failed Tests}\n')
	for r in results:
		if r.get('success'):
			continue
		f.write('\\subsection{'+r.get('name')+'}\n')
		f.write('\\begin{tabular}{|p{.3\\textwidth-2\\tabcolsep} |p{.7\\textwidth-2\\tabcolsep} |} \\hline\n')
		for k, v in r.attributes.items():
			f.write(translate(str(k)) + ' & ' + translate(str(v)) + ' \\\\ \\hline \n')
		f.write('\\end{tabular}\n')
	f.write('\\end{document}')





