import os
import pygame
from pygame.locals import *
import pygbutton
import fborx
import math

pygame.init()

#add the text for your buttons here, feel free to make the array longer or shorter
texts = ['system halt','settings','xserver','a','b','c','d','e','f']

#add your commands for the buttons here in the same order as your texts
#be carefull what commands you add, since they might be executed by mistake by users
functions = ['sudo halt','sudo raspi-config','startx','echo a','echo b','echo c','echo d','echo e','echo f']

#edit the button size here
buttonSize = [100,50]

#how many buttons you want in one row?
columns = 3

#number of rows will be determined by the number of buttons
buttonCount = len(texts)
rows = int(math.ceil(1.0*buttonCount/columns))

#create a button array
buttons = []
for i in range(0,buttonCount):
	buttons.append(pygbutton.PygButton(Rect((i%columns)*buttonSize[0],(i/columns)*buttonSize[1],buttonSize[0],buttonSize[1]), texts[i]))

while True:
	# this will open a window if xserver is running or fullscreen fb if not
	#screen = fborx.getScreen(buttonSize[0]*columns,buttonSize[1]*rows)
	screen = fborx.getScreen(800, 600)

	#since there is no mouse hover effect or something, we only need to draw them once
	for button in buttons:
		button.draw(screen)
	pygame.display.flip()

	running = True
	cmd = ''

	while running:
		for event in pygame.event.get(): # event handling loop
			if event.type == pygame.KEYDOWN:
        			if event.key == K_ESCAPE:
					pygame.quit()
					os._exit(0) #exit the program

			for i in range(0,buttonCount):
				if 'click' in buttons[i].handleEvent(event):
					cmd = functions[i]
					running = False


	#quit pygame so we get our fb back
	pygame.quit()

	print(cmd) #for debug
	os.system(cmd) #run the cmd. Put a # in front of this line for debug

	#re init pygame to show the gui again
	pygame.init()
