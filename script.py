#!/usr/bin/python3
import os

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
			
	

