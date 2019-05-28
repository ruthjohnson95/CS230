import json
import subprocess

def run (command):
	print(command)
	pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return pipes.communicate()

with open('insecure_full.json') as json_file:  
	data = json.load(json_file)
	i = 0
	for key in data:
		print ("\nlibrary", i, key)
		print("version is ", data[key][0]['v'])
		std_out, std_err = run(["pip", "download", "--no-deps", "--no-binary", ":all:",  "-d", "../../../libraries",  key+data[key][0]['v']])
		print(std_out.decode('utf-8'))
		print(std_err.decode('utf-8'))

#		#if i >= 20:
#		#	break
		i = i + 1