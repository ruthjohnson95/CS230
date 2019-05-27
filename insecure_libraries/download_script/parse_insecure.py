import json
import subprocess


# openslides
# 

def run (command):
	print(command)
	pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return pipes.communicate()
	#return None, None
	
#def v1_gt_v2(v1, v2):
#	version1 = v1.split(".")
#	version2 = v2.split(".")
	
#	idx1 = 0
#	idx2 = 0
	
#	while idx1 < len(version1) or idx2 <len(version2):
#		s1 = "0"
#		s2 = "0"
#		if idx1 < len(version1):
#			s1 = version1[idx1]
			
#		if idx2 <len(version2):
#			s2 = version2[idx2]
			
#		try:
#			if int(s1) < int(s2):
#				#print("v1 is smaller at idx: ", idx1)
#				return False
#			elif int(s1) > int(s2):
#				#print("v1 is larger at idx: ", idx1)
#				return True

#		except:
#			if s1 < s2:
#				#print("v1 is smaller at idx: ", idx1)
#				return False
#			elif s1 > s2:
#				#print("v1 is larger at idx: ", idx1)
#				return True
				
#		idx1 = idx1 + 1
#		idx2 = idx2 + 1
	
#	print("v1 and v2 are exactly the same")		
#	return 0
	
#def first_in_list_lt_secure_version (versions, secure_version, key):
#	found = False
#	for v in reversed(versions):
#		if v1_gt_v2(secure_version, v):
#			print ("secure version: ", secure_version )
#			print ("getting version: ", v)
#			command = ["pip", "download", key+"=="+v]
#			print(command)
#			#run (command)
#			print(versions)
#			found = True
#			break
						
#	if not found:
#		print ("all available versions greater than secure version")
#		print ("secure version: ", secure_version )
#		print(versions)

with open('insecure_full.json') as json_file:  
	data = json.load(json_file)
	i = 0
	for key in data:
		print ("\nlibrary", i, key)
		print("version is ", data[key][0]['v'])
		#print("data[key][0] is ", data[key][0])
		#print("data[key] is ", data[key])
		std_out, std_err = run(["pip", "download", "--no-deps", "--no-binary", ":all:",  "-d", "../../../libraries",  key+data[key][0]['v']])
		print(std_out.decode('utf-8'))
		print(std_err.decode('utf-8'))
#		std_out, std_err = run(["pip", "download", key+"=="])
#		output = std_err.decode('utf-8')
#		if "(" in output and ")" in output and "none" not in output:
#			start = output.find("(from versions: ")
#			end = output.find(')')
#			versions = output[start+16:end].split(", ")
#			
#			if len(data[key][0]["specs"]) > 1:
#				print ("too many versions")
#			else:
#				secure_version = data[key][0]["specs"][0]
#				
#				if secure_version[0] == '<' and secure_version[1] == '=': 
#					secure_version = secure_version[2:]
#					if secure_version in versions:
#						print ("(in)secure version: ", secure_version )
#						print ("getting version: ", secure_version)
#						command = ["pip", "download", key+"=="+secure_version]
#						print(command)
#						#run (command)
#					else:
#						first_in_list_lt_secure_version (versions, secure_version, key)
#						
#				elif secure_version[0] == '<':
#					secure_version = secure_version[1:]
#					if secure_version in versions:
#						idx = versions.index(secure_version)
#						if idx > 0:
#							print ("secure version: ", secure_version )
#							print ("getting version: ", versions[idx-1])
#							command = ["pip", "download", key+"=="+versions[idx-1]]
#							print(command)
#							#run (command)
#						else:
#							print ("secure version is already oldest version")
#							print ("secure version: ", secure_version )
#							print (versions)
#					else:
#						#print ("!!secure version not available!!")
#						first_in_list_lt_secure_version (versions, secure_version, key)
#			
#				else:
#					print ("version not <, cannot handle")
#		else:
#			#print ("pip cannot find", std_err.decode('utf-8'))
#			print ("pip cannot find")
#		#if i >= 20:
#		#	break
		i = i + 1