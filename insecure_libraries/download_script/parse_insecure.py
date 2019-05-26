import json
import subprocess


def run (command):
	pipes = subprocess.Popen(["pip", "download", key+"=="], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return pipes.communicate()

with open('insecure_full.json') as json_file:  
	data = json.load(json_file)
	i = 0
	for key in data:
		
		std_out, std_err = run(["pip", "download", key+"=="])
		output = std_err.decode('utf-8')
		if "(" in output and ")" in output and "none" not in output:
			start = output.find("(from versions: ")
			end = output.find(')')
			versions = output[start+16:end].split(", ")
			
			if len(data[key][0]["specs"]) > 1:
				print ("too many versions")
			else:
				secure_version = data[key][0]["specs"][0]
				if secure_version[0] == '<':
					if secure_version[1:] in versions:
						idx = versions.index(secure_version[1:])
						if idx > 0:
							print ("secure version: ", secure_version[1:] )
							print ("getting version: ", versions[idx-1])
							command = ["pip", "download", key+"=="+versions[idx-1]]
							print(command)
							#run (command)
						else:
							print ("secure version is already oldest version")
							print ("secure version: ", secure_version[1:] )
							print (versions)
					else:
						print ("!!!!!!!!!!!!!secure version not available!!!!!!!!!!!!!!")
						print ("secure version: ", secure_version[1:] )
						print ("getting version: ", versions[-1])
						command = ["pip", "download", key+"=="+versions[-1]]
						print(command)
						#run (command)
						print(versions)
					
				else:
					print ("version not <, cannot handle")
		else:
			#print ("pip cannot find", std_err.decode('utf-8'))
			print ("pip cannot find")
		#if i >= 20:
		#	break
		#i = i + 1