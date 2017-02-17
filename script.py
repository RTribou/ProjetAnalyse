#!/usr/bin/python3
import os
#command line to get asm code from specify sections: objdump -sj.data -sj.text 0a6c6d1b3e8db37a621aad7fba82501c79cd473b146144af7e54a4bfcccc0ff6

if __name__ == '__main__':
	current_wd = os.getcwd()
	print('Current Working Directory: ' + current_wd)
	list_files= os.listdir(current_wd)

	for filename in list_files:
		if '.' in filename:
			print(filename + ' is not a binary')
			list_files.remove(filename)
			print(filename + ' has been removed from listfile')

	for filename in list_files:
		print(filename)
			
	

