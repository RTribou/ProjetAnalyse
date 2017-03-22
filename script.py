#!/usr/bin/python3
import os
import subprocess
import binascii
import codecs
import math
import sys
#command line to get asm code from specify sections: objdump -sj.data -sj.text 0a6c6d1b3e8db37a621aad7fba82501c79cd473b146144af7e54a4bfcccc0ff6
#objdump -h ch1.bin -> parser le resultat pour recuperer les sections
#objcopy -O binary --only-section=.text ch1.bin output.bin -> recuperer le code asm d'une section precise
#utiliser les tuples ou dico : binary[nom_section]=asm
#puis calcul de l'entropie des sections qu'on enregistre dans le tuple a la place du code asm puis sauvegarde un un fichier nom_fichier.entropy

#recupere les noms des sections: objdump -h ch1.bin | gawk '{if (NR % 2 ==0) print $2}' | sed -n '3,$p'
#dictionnaire: http://apprendre-python.com/page-apprendre-dictionnaire-python

#Funtion getHexaFromFile:
#Recupere sous forme hexadecimal le contenu du fichier
#
def getHexaFromFile(datafile):
	buffer=""
	for chunk in iter(lambda: datafile.read(32), b''):
			#On nettoie le buffer
			tmp=str(codecs.encode(chunk, 'hex'))
			tmp=tmp.replace("b'", '')
			tmp=tmp.replace("'", '')
			#Et on concatene
			buffer=buffer+tmp

	return buffer
#----------------------------------------------------------
def analyseByBlocks(list_files):
	for filename in list_files:
		print("Nom du fichier: "+filename)

		#Fichier Pour contenir le code du programme
		tmp_output=openFile("/tmp/output", 'rb')

		tmp_file=open(filename,'rb')
		#On recupere le binaire sous formes Hexadecimal
		buffer=getHexaFromFile(tmp_file)

		#128bits= bloc de 32 caracteres

		sizeBlock=128/4

		binarySize=len(buffer)
		nbBlock=int(binarySize/sizeBlock)+1
		info_entropy=""
		print("[+] File: "+filename+ " - Size= " + str(binarySize) + " - Block size= "+str(sizeBlock)+ " - Number of block= " + str(nbBlock))
		for i in range(0,nbBlock):
			tmp_buffer=buffer[int(i*sizeBlock): int(i*sizeBlock+32)]
			info_entropy=info_entropy+ str(entropy_shannon(tmp_buffer)) + '\n'
		#End for
		info_entropy="blocks ; "+str(nbBlock)+'\n'+info_entropy
		tmp_entropy_file=openFile(os.getcwd()+"/"+filename+".ent", 'w')
		tmp_entropy_file.write(info_entropy)
		tmp_entropy_file.close()
	#EndFor
#----------------------------------------------------------
def analyseBySections(list_files):
	for filename in list_files:
		print("Nom du fichier: "+filename)

		#Recupere la liste de toute les sections
		os.system("objdump -h "+ filename +" | gawk '{if (NR % 2 ==0) print $2}' | sed -n '3,$p' > /tmp/project ")
		#Fichier contenant la liste des sections du l'executable
		tmp_file=open("/tmp/project", 'r')

		#Fichier Pour contenir le code des sections
		tmp_output=openFile("/tmp/output", 'rb')

		section_list=tmp_file.readlines()
		#Variable globale
		info_entropy="" #Ensemble des lignes qu'il faudra copier
		size=0
		for line in section_list:
			tmp_info_ent=""#Represente une ligne
			tmp_output=open("/tmp/output", 'rb')
			if '\n' in line:
				line=line.replace('\n', '')

			os.system("objcopy -O binary --only-section="+ line +" "+ filename +  " /tmp/output")

			tmp=getHexaFromFile(tmp_output)

			size=size+len(tmp)

			tmp_info_ent=line+ ";" + str(entropy_shannon(tmp))+ ";"+ str(len(tmp))+'\n'
			info_entropy=info_entropy+tmp_info_ent

			tmp_output.close()
			#on vide le fichier temporaire
			with open("/tmp/output", 'w'): pass
			#tmp_output.read()
		#End for sections_list

		#ON creer le fichier si il n'existe pas et on ajoute les infos
		info_entropy=str(size)+'\n'+info_entropy
		tmp_entropy_file=openFile(os.getcwd()+"/"+filename+".ent", 'w')
		tmp_entropy_file.write(info_entropy)
		tmp_entropy_file.close()
#----------------------------------------------------------
def entropy_shannon(data):
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(chr(x)))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy
#----------------------------------------------------------
#Funtion openFile:
#Check if 'path' is a file and create it if is not
#Open 'path'
#	Param:
#		path: path of the file you want to open
#		mode: type of acces mode ('read', 'write')
#
def openFile(path, mode):
	if not os.path.isfile(path):
		tmp_file=open(path,"x")

	tmp_file=open(path, mode)
	return tmp_file
#----------------------------------------------------------
if __name__ == '__main__':
	current_wd = os.getcwd()
	print('[+]Current Working Directory: ' + current_wd)
	list_files= os.listdir(current_wd)

	for filename in list_files:
		res=os.popen('file -i ' + filename).readlines()#application/x-executable; charset=binary

		if "application/x-executable; charset=binary" in res[0]:#Detection des binaires
			print ("[+]Executable binary: "+ filename)
		else:
			list_files.remove(filename)

	#End for

	if len(sys.argv)==2:
		if sys.argv[1]=="--blocks":
			print("[+]Analyse par bloc")
			analyseByBlocks(list_files)
		else:
			print("[-]Error")
	else:
		print("[+]Analyse sections par sections")
		analyseBySections(list_files)
	'''for filename in list_files:
		print("Nom du fichier: "+filename)

		#Recupere la liste de toute les sections
		os.system("objdump -h "+ filename +" | gawk '{if (NR % 2 ==0) print $2}' | sed -n '3,$p' > /tmp/project ")
		#Fichier contenant la liste des sections du l'executable
		tmp_file=open("/tmp/project", 'r')


		#Fichier Pour contenir le code des sections
		tmp_output=openFile("/tmp/output", 'rb')

		section_list=tmp_file.readlines()
		#Variable globale
		info_entropy=""
		size=0
		for line in section_list:
			tmp_info_ent=""
			tmp_output=open("/tmp/output", 'rb')
			if '\n' in line:
				line=line.replace('\n', '')

			os.system("objcopy -O binary --only-section="+ line +" "+ filename +  " /tmp/output")

			tmp=""
			for chunk in iter(lambda: tmp_output.read(32), b''):
				#On nettoie le buffer
				 tmp2=str(codecs.encode(chunk, 'hex'))
				 tmp2=tmp2.replace("b'", '')
				 tmp2=tmp2.replace("'", '')
				 #Et on concatene
				 tmp=tmp+tmp2
			#End for
			#print(line+ " ; " + tmp+ " ; "+ str(len(tmp)))
			size=size+len(tmp)

			tmp_info_ent=line+ ";" + str(entropy_shannon(tmp))+ ";"+ str(len(tmp))+'\n'
			info_entropy=info_entropy+tmp_info_ent

			tmp_output.close()
			#on vide le fichier temporaire
			with open("/tmp/output", 'w'): pass
			#tmp_output.read()
		#End for sections_list

		#ON creer le fichier si il n'existe pas et on ajoute les infos
		info_entropy=str(size)+'\n'+info_entropy
		tmp_entropy_file=openFile(os.getcwd()+"/"+filename+".ent", 'w')
		tmp_entropy_file.write(info_entropy)
		tmp_entropy_file.close()
	#End for each file'''
