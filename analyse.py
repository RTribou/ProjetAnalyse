#!/usr/bin/python3

import glob
import os
import scipy.misc
import numpy as np
from PIL import Image
list_entropy_file=glob.glob("*.ent")

width=600
height=800
def drawPixelEntropy(img, x, y, entropy):
	if entropy < 2:
		img[x,y]=(0,255,0)
	elif entropy < 4:
		img[x,y]=(255,255,0)
	elif entropy < 6:
		img[x,y]=(255,0,0)
	else:
		img[x,y]=(0,0,0)



def analyseBySections(filename, tmp_file, size):
	img = Image.new( 'RGB', (width,height), "white") # create a new black image
	pixels = img.load() # creat
	print("Fichier: "+ent_file + " Taille totale : "+str(size))
	start_draw=0
	for line in tmp_file:
		if '\n' in line:
			line=line.replace('\n', '')
		data=line.split(';')

		height_of_section=round(int(data[2])*height / int(size))

		print("Section: " + data[0] + " - Taille: " + data[2] + " Nb Pixel: " +str(height_of_section))

		for x in range(img.size[0]):

			t=range(int(start_draw),int(start_draw+height_of_section))
			#print(t)
			for y in t:
				drawPixelEntropy(pixels,x, y, float(data[1]))
				#print("x "+str(x) +" y "+str(y))

		start_draw=start_draw+height_of_section

	#img.show()
	img.save(filename[0:len(filename)-3]+"jpeg","jpeg")

def analyseByBlocks(filename, tmp_file, info_file):

	img = Image.new( 'RGB', (width,height), "black") # create a new black image
	pixels = img.load() # creat

	nbBlocks=int(info_file.split(';')[1])
	print("[+]Nb blocks: "+str(nbBlocks))
	nbpixel=width*height
	nb_pixel_per_block=int(nbpixel/nbBlocks)

	tmp_line=0
	tmp_pixel=0
	for line in tmp_file:

		#drawBlock(pixels, line, nb_pixel_per_block)
		for x in range(nb_pixel_per_block):
			#pixels[tmp_pixel,tmp_line]=color
			drawPixelEntropy(pixels, tmp_pixel, tmp_line, float(line))
			#print(str(tmp_line) + " - "+ str(tmp_pixel))
			tmp_pixel=tmp_pixel+1
			if tmp_pixel==width:
				tmp_line=tmp_line+1
				tmp_pixel=0

	#img.show()
	img.save(filename[0:len(filename)-4]+"-blocks.jpeg","jpeg")

for ent_file in list_entropy_file:
	# Create an empty image
	img = Image.new( 'RGB', (width,height), "black") # create a new black image
	pixels = img.load() # create the pixel map

	tmp_file=open(ent_file, 'r')
	info_file=tmp_file.readline()
	if "blocks" in info_file:
		print ("[+]"+ ent_file +" -> Analyse by blocks")
		analyseByBlocks(ent_file,tmp_file, info_file)
	else:
		print ("[+]"+ ent_file +" -> Analyse by sections")
		analyseBySections(ent_file, tmp_file, info_file)


'''def analyseByBlocks(tmp_file, info_file):
		print(info_file.split(';'))

	def analyseBySections(tmp_file, size):
		print("Fichier: "+ent_file + " Taille totale : "+str(size))
		start_draw=0
		for line in tmp_file:
			if '\n' in line:
				line=line.replace('\n', '')
			data=line.split(';')

			height_of_section=round(int(data[2])*height / int(size))

			print("Section: " + data[0] + " - Taille: " + data[2] + " Nb Pixel: " +str(height_of_section))

			if float(data[1])<=3:
				color=[0,255,2]
			elif float(data[1])<=5:
				color=[255,255,0]
			else:
				color=[255,0,0]


			for x in range(img.size[0]):

				t=range(int(start_draw),int(start_draw+height_of_section))
				print(t)
				for y in t:
					if float(data[1])<=3:
						pixels[x,y]=(0,255,0)
					elif float(data[1])<=5:
						pixels[x,y]=(255,255,0)
					else:
						pixels[x,y]=(255,0,0)
					#print("x "+str(x) +" y "+str(y))

			start_draw=start_draw+height_of_section

		img.show()'''
