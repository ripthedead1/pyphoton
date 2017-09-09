#!/usr/bin/env python3

# -*- coding: utf-8 -*

#nformation : utilisation des port pat GPIO et non par PIN !!
#le bouton doit etre connecter sur la PIN 6 -> GPIO18

#version 1.0 -> 1.2 ----------------------
# format des photos : w 1024 h 768
#Ajout de la gestion des LED - Bouton
#LED 1 Bouton Vert Valider/recommancer
#LEd 2 Bouton Rouge Annuler/quitter 
#ajout dela gestion du relais pour le Flash en Rubant led ...
#version 1.3 -------------------
#Travail sur l'interface graphique ....
#version 1.4 --------------------
# ajour de la fonction wallpaper ....
#changement des chemain pour les img du prog

#<--------------- Declaration des librairies -------------->

import RPi.GPIO as GPIO

import time, sys, signal
from datetime import datetime

from PIL import Image

import pygame
from pygame.locals import *

import os
import PIL.Image
import PIL.ImageEnhance

#<--------------- Declaration des var -------------->
ver=1.4

pygame.init()

 #LED pour le bouton Vert - GPIO17
led_1 =17
 #LED pouir le bouton Rouge - GPIO27
led_2 =27
 #Flah gerer par le relais  - GPIO10
flash_led =22
 #Bouton vert - GPIO25
Bouton_vert =25
 #Bouton Rouge - GPIO8
Bouton_Rouge =8

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#screen = pygame.display.set_mode((640, 480))
 
width, height = screen.get_size()


position_mem =0 #compteur des photos
affiche =["-","-","-","-","-"] # memoire des 5 dernieres photo
WaitTime =10 #delay avant l 'activation du mure d image ...

#chem_orig='/home/pi/PiPhotos/'	# definie le chemin detravail ! modif ici si travaill ailleur ! 
chem_orig='/media/pi/py/PyPhoton/' #stockage sur cle usb :)
logo = '/home/pi/script/back1.png'	# indique ici ou trouver le logo
splash='/home/pi/script/splash.png'	#indiqe ou se trouve mon logo de demm 
demarage =0						#temoin de lencement 0 = debut 

#<--------------- Initialisation des Ports GPIO -------------->

GPIO.setmode(GPIO.BCM)			#Attention fonctionement en mode GPIO et non ar Pin !!!!
GPIO.setwarnings(False)			#desactivation des fausse erreur 
# passage des Port GPIO a l'etat bas 
GPIO.setup(led_1, GPIO.OUT, initial =GPIO.LOW)
GPIO.setup(led_2, GPIO.OUT, initial =GPIO.LOW)
GPIO.setup(flash_led, GPIO.OUT, initial =GPIO.LOW)

#Passage en mode PUll_down pour les Bouttons
GPIO.setup(Bouton_vert, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#Pour GPIO25 --> Boutton VERT
GPIO.setup(Bouton_Rouge,GPIO.IN, pull_up_down=GPIO.PUD_UP)	#Pour GPIO8  --> Boutton ROUGE

#<--------------- debut du code  -------------->
print("+------------------------+")
print("|    PyPhoto By Vivian   |")
print("|    version",ver)
print("+------------------------+")
print(" ")
print("<------------------->")
print("Resolution :",width," x ",height)


#desactiver pour l'instant car bug :(
#def signal_handler(signal, frame): # gestion de l'interuption via CRLT-C
#	print ("You pressed Ctrl+C!")
#	sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)
#print ("Press Ctrl+C")
#signal.pause()

#Introduction de lancement ....
def introduction():
	print("<------------------->")
	print("chemin slpash screen : "+splash)
	print("<------------------->")
	
#pour centrer img  [largeur ecran/2 - largeur img/2, hauteur/2 - hauteur/2])
	
	spl = pygame.image.load(splash).convert()	#chargement tu tag/filtre
	img_larg = spl.get_width()					# On récupère les dimensions de l'img
	img_haut = spl.get_height()					
	
	screen.blit(spl,(width/2 - img_larg/2, height/2 - img_haut/2))
	pygame.display.flip()#rafraichissement de l'ecran ...
	time.sleep(10)
	

	
def on_led(led): #Passe le Port GPIO a l'etat Haut
    print ("--> Allume la LEd : ",led)
    GPIO.output(led, GPIO.HIGH) #Change l'etat du port GPIO 

def off_led(led): #Passe le Port GPIO a l'etat bas
    print ("--> Eteind la LEd : ",led)
    GPIO.output(led, GPIO.LOW) #Change l'etat du port GPIO 

def clig_led(led): #Changement de l'etat du port GPIO 
    print ("--> Clignote la LEd ",led)
    GPIO.output(led, not GPIO.input(led))
    
def flash_on(): #On allume le Flash
	print ("--> Allume le Flash")
	GPIO.output(flash_led, GPIO.HIGH) #Active Le Flash 
    
def flash_off(): #On eteind le flash
	print ("--> Eteind le Flash")
	GPIO.output(flash_led, GPIO.LOW) #desactive Le Flash 

def takepic(imageName): #prend une photo (note: il faut selectionner la ligne qui correspond votre installation en enlevant le premier)
	#Activation du flash pour la Photo 
	flash_on()
	command ='raspistill -w 1024 -h 768 -o '+imageName #prend une photo
	# command = "sudo raspistill -w 960 -h 720 -o "+ imageName +" -rot 90 -q 80" #prend une photo et la tourne de 90
	# command = "sudo raspistill -w 960 -h 720 -o "+ imageName +" -rot 180 -q 80" #prend une photo et la tourne de 180
	# command = "sudo raspistill -w 960 -h 720 -o "+ imageName +" -rot 270 -q 80" #prend une photo et la tourne de 270
	
	#desactivation du flash 
	
	os.system(command)#commande qui prend la photo ...
	command = 'cp '+imageName+' '+imageName+'_tag.jpg'
	print(command)
	os.system (command)#comande qui duplique la photo avec la mention tag.jpg
	command ='mv '+imageName+' '+imageName+'.jpg'
	os.system(command)#commande qui renome avec la bonne extention
	print("-> Photo prise ...")
	print(" --> Resultat :"+imageName)

def loadpic(imageName): #travail sur la photo ....
	print("<------------------->")
	print("--> Image charger  :"+imageName)
	print("--> logo à charger :"+logo)
	
	print("debut travail sur photo ...")

	background = pygame.image.load(imageName).convert() #chargement de l image
	screen.blit(background,(0,0),(0,0,width,height))#affiche la photo en fond
	print("-----> Affichage Photo ...")
	tag = pygame.image.load(logo).convert_alpha() #chargement tu tag/filtre
	screen.blit(tag,(0,0))#affiche le tag par dessus
	print("-----> Affichage du filtre")
	#screen.blit(tag,(10,10,width,height))#affiche le tag par dessus
	#background = pygame.transform.scale(background,(width,height))
	
	pygame.display.flip()#rafraichissement de l'ecran ...
	print("-----> Capture du resultat et sav")
	pygame.image.save(screen,imageName)#sav de l'affichage ....upgate de la photo tager
	time.sleep(3)#tempo de visualisation 
	
def minuterie(): #ajout de la fonction clig_led(led) pour le bouton rouge
	clig_led(led_2)
	writemessage("- 3 -")
	time.sleep(1)
	clig_led(led_2)
	writemessage("- 2 -")
	time.sleep(1)
	clig_led(led_2)
	writemessage("- 1 -")
	time.sleep(1)
	clig_led(led_2)
	writemessage("- Cheese :) -")
	time.sleep(1)

def writemessage(message): # pour pouvoir afficher des messages sur un font noir 
	screen.fill(pygame.Color(0,0,0))
	BLACK = pygame.Color(255,215,0)	
	font = pygame.font.SysFont("verdana",50,bold=1)
	text = font.render(message, True, BLACK) 
	text_rect = text.get_rect(center=(width/2, height/2))
	screen.blit(text, text_rect)
	pygame.display.update()

	
	#font = pygame.font.SysFont("verdana", 50, bold=1)
	#textsurface = font.render(message, 1, pygame.Color(255,255,255))
	#screen.blit(textsurface,(35,40)) #original
	#pygame.display.update()

def writemessagetransparent(message): # pour pouvoir afficher des messages en conservant le font 
	font = pygame.font.SysFont("verdana", 50, bold=1)
	textsurface = font.render(message, 1, pygame.Color(255,255,255))
	screen.blit(textsurface,(35,40))
	pygame.display.update()

if (os.path.isdir(chem_orig) == False): #si le dossier pour stocker les photos n'existe pas       
	os.mkdir(chem_orig)                  #alors on cree le dossier (sur le bureau)
	os.chmod(chem_orig,0o777)            #et on change les droits pour pouvoir effacer des photos


while True : #boucle jusqu'a interruption
	try:
		if (demarage == 0):
			demarage=1 #evite de recomancer un seconde fois
			introduction()
		print("<------------------->")		
		print("Mode debug actif ....")#Pour le debug & dev ....
		print(" ")
		print("En attente...")#on attend que le bouton soit pressé
		
		writemessage("Une P'tite Photo ? -Press Bouton vert -")
		
		on_led(led_1) # Active la led Vert ...
		now=time.time()
		#while (GPIO.input(Bouton_vert)==1 and time.time()-now<WaitTime):
		#	time.sleep(0.1) #save the cpu from running at 100%
		GPIO.wait_for_edge(Bouton_vert, GPIO.FALLING) #on a appuyersur le bouton vert !!!!
		off_led(led_1) #eteint la led ...
		
		print("Activation ! Prise de la photo amorcer ...")
		
		#on genere le nom de la photo avec heure_min_sec
		date_today = datetime.now()
		nom_image = date_today.strftime('%d_%m_%H_%M_%S')
		print("Generation du nom de la photo : "+nom_image)
		chemin_photo = chem_orig+nom_image#on defini le chemain de la photo
		print("Chemin complet : "+chemin_photo) 
		
		minuterie() #on lance le decompt
		
		takepic(chemin_photo) #sourier ! c'est dans la boite ! :)
		
		photo = chemin_photo+'.jpg' #ceci est la photo classique 
		photo_tag = chemin_photo+'_tag.jpg' #ajout de l indicateur tag pour la photo avec filtre
		
		print("<------------------->")
		print("Pour resumer : 2 photo en sortie ")
		print("--> Photo normale    :"+photo)
		print("--> Photo tagger     :"+photo_tag) 
		print("--> Logo pour le Tag :"+logo)
		flash_off()
		writemessage("Traitement en cours ...")	
			
		loadpic(photo_tag) #on affiche la photo final 
		affiche [position_mem] = photo_tag
		
		#if on ajout la photo toutes fraiche dans la liste ... 
		#if (position_mem <= 5): #test si position_mem <= a 5 ...
		#	position_mem = position_mem +1
		#else:
		#	position_mem =0
		#debug
		#print ("Photo en memoire ...")
		#print(affiche [0])
		#print(affiche [1])
		#print(affiche [2])
		#print(affiche [3])
		#print(affiche [4])
		
		print("<------------------->")
		print("Travaille Terminer ...")
		on_led(led_2) # Active la led_rouge  ...
		writemessage("Patienter SVP ") #on affiche un message
		time.sleep(2)
		off_led(led_2)#desactive la led avant recommencer le cycle ...
		
		if (GPIO.input(Bouton_Rouge) == 0): #si le bouton est encore enfonce (sont etat sera 0)
			print("Good Bye ...")
			#partie qui ferme les pin
			GPIO.output(led_1, GPIO.LOW)
			GPIO.output(led_2, GPIO.LOW)
			#GPIO.cleanup() # attention met a l'etat haut !!!
			break #alors on sort du while
			 
	except KeyboardInterrupt: # Ne parche pas .... :( 
		print ("sortie du programme!")
		raise
		GPIO.cleanup()           #reinitialisation GPIO lors d'une sortie normale
		sys.exit(0)
