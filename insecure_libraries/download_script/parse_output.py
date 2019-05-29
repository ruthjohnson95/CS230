file = open('output_linux.txt', 'r')
line = file.readline()
lib = False
library = ''
count = 0

print ("missing libraries:\n")
while line:
	if 'library ' in line:
		if lib:
			print (library)
			count = count + 1
			
		lib = True
		line = line[8:]
		index = line.find(' ')
		library = line[index+1:]
		
	if 'Saved ' in line:
		lib = False
		
	line = file.readline()
	
print ("total missing libraries:", count)
file.close()
