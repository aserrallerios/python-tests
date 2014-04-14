import sys
import re
from os import listdir
from os.path import isfile, join

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def special_keys(key):
	return key.replace('next','button_next').replace('previous','button_back')

onlyfiles = [ f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1],f)) ]

for (file) in onlyfiles:
	with open(sys.argv[2] + '/' + file.title().lower().replace('indexpagebean_','defaults.').replace('indexpagebean','defaults').replace('_','-').replace('.properties','.js'),'w+') as outputFile:

		outputFile.write('(function(){var fn = function(){return{\n');
		with open(sys.argv[1] + file, 'r') as f:
			for line in f:
				if not line.startswith('MessagesHeader'):
					line = line.decode('unicode_escape').encode('utf8').replace('\n','')#.replace('{0}','<%=params[0]%>')
					if len(line) > 1 :
						keyValue = line.split('=')
						outputFile.write('{0:<30} : {1}'.format('"' + special_keys(convert(keyValue[0].strip())) + '"','"' + keyValue[1].strip() + '",\n'))
		with open(sys.argv[1] + 'dynamic/' + file.replace('IndexPageBean','ErrorPageBean')) as errorf:
			for line in errorf:
					line = line.decode('unicode_escape').encode('utf8').replace('\n','')
					if len(line) > 1 :
						keyValue = line.split('=')
						outputFile.write('{0:<30} : {1}'.format('"' + convert(keyValue[0].strip()) + '"','"' + keyValue[1].strip() + '",\n'))
		outputFile.write('{0:<30} : {1}'.format('"title"','"",\n'))
		outputFile.write('}};if( typeof define !== "undefined" ) define([], fn); else module.exports = fn;})();')