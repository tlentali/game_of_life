#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import Tkinter
import tkSimpleDialog
from Tkinter import Tk, Canvas, Button, Frame, BOTH, NORMAL, HIDDEN, StringVar, IntVar
from Tkinter import *
from tkFileDialog import askopenfilename
# ------------------------------------------------------------------------------
#permet lire les coordonnés de la souris
    
def interpret(e):
    if e.y > 500 :
        e.y = 500
    if e.y < 3 :
        e.y = 3
    ii = (e.y-3) // cell_size
    if e.x > 500 :
        e.x = 500
    if e.x < 3 :
        e.x = 3
    jj = (e.x-3) // cell_size

    canvas.itemconfig(cell_matrix[addpoint(ii, jj)], state=NORMAL, tags='vis')
 # ------------------------------------------------------------------------------
def addpoint(ii,jj):
    if(ii < 0 or jj < 0 or ii >= field_height or jj >= field_width):
        return len(cell_matrix)-1
    else:
        return ii * (win_width // cell_size) + jj
# ------------------------------------------------------------------------------
def nextGeneration():
    global vie, mort
    #print new_vie.get()
    #print new_mort.get()

    for i in range(field_height):
        for j in range(field_width):
            k = 0
            for i_shift in range(-1, 2):
                for j_shift in range(-1, 2):
                    if (canvas.gettags(cell_matrix[addpoint(i + i_shift, j + j_shift)])[0] == 'vis' and (i_shift != 0 or j_shift != 0)):
                        k += 1
            current_tag = canvas.gettags(cell_matrix[addpoint(i, j)])[0]

            if(canvas.gettags(cell_matrix[addpoint(i, j)])[0] == 'hid'):
               if(vie[k]=="1"):
                  canvas.itemconfig(cell_matrix[addpoint(i, j)], tags=(current_tag, 'to_vis'))
               else:
                 canvas.itemconfig(cell_matrix[addpoint(i, j)], tags=(current_tag, 'to_hid'))
            if(canvas.gettags(cell_matrix[addpoint(i, j)])[0] == 'vis'):
                if(mort[k]=="1"):
                     canvas.itemconfig(cell_matrix[addpoint(i, j)], tags=(current_tag, 'to_vis'))
                else:
                     canvas.itemconfig(cell_matrix[addpoint(i, j)], tags=(current_tag, 'to_hid'))
# ------------------------------------------------------------------------------
#permet de generer la nouvelle generation et de l''afficher
def step():
    nextGeneration()
    repaint()
# ------------------------------------------------------------------------------
#efface les cellules vivantes dans le canvas
def clear():
    for i in range(field_height):
        for j in range(field_width):
            canvas.itemconfig(cell_matrix[addpoint(i, j)], state=HIDDEN, tags=('hid','0'))
# ------------------------------------------------------------------------------
#met a jour le canvas
def repaint():
	for i in range(field_height):
		for j in range(field_width):
			if (canvas.gettags(cell_matrix[addpoint(i, j)])[1] == 'to_hid'):
				canvas.itemconfig(cell_matrix[addpoint(i, j)], state=HIDDEN, tags=('hid','0'))
			if (canvas.gettags(cell_matrix[addpoint(i, j)])[1] == 'to_vis'):
				canvas.itemconfig(cell_matrix[addpoint(i, j)], state=NORMAL, tags=('vis','0'))
# ------------------------------------------------------------------------------
#dessine un planeur dans le canvas
def planer():
    clear()
    canvas.itemconfig(cell_matrix[addpoint(7, 8)], state=NORMAL, tags='vis')
    canvas.itemconfig(cell_matrix[addpoint(8, 7)], state=NORMAL, tags='vis')
    canvas.itemconfig(cell_matrix[addpoint(9, 9)], state=NORMAL, tags='vis')
    canvas.itemconfig(cell_matrix[addpoint(9, 8)], state=NORMAL, tags='vis')
    canvas.itemconfig(cell_matrix[addpoint(9, 7)], state=NORMAL, tags='vis')
# ------------------------------------------------------------------------------
#met le programme en pause quand il est en mode "automatique"
def pause():
    global compteur, iteration
    if compteur % 2 == 0:
        stop = 1
        compteur += 1
        iteration = 0
        automatique()
    else:
        stop = 0
        compteur -= 1
        iteration = 200
        automatique()
# ------------------------------------------------------------------------------
#active le mode automatique de la generation des generations
def automatique():
    global cmmp
    if stop==0 and cmmp<=iteration:
        nextGeneration()
        repaint()
        cmmp+=1
        root.after(50,automatique)
    else:
        cmmp=0
# ------------------------------------------------------------------------------
#ouvre une fenetre et propose a l'utilisateur d'ouvir un fichier txt contenant une matrice et l'affiche dans le canvas
def file_to_open():
    file_path = askopenfilename()
    clear()
    try:
        ofi = open(file_path, 'rb')
    except:
        tkMessageBox.showwarning(
            "Open file", "Cannot open this file: (%s)\n" % file_path)
    compteur1 = 0
    for text in ofi:
        elt = text.split(' ')
        compteur2 = 0
        for x in range(len(elt)):
            if int(elt[int(x)]) == 1:
                canvas.itemconfig(cell_matrix[addpoint(compteur1, compteur2)], state=NORMAL, tags='vis')
            compteur2 += 1
        compteur1 += 1
# ------------------------------------------------------------------------------
# nouvelle regles entré par l'utilisateur
def new_rules():
    global e1, e2, new_vie, new_mort, ask_rules
    ask_rules = Tkinter.Toplevel(root)
    ask_rules.title('New Rules')
    ask_rules.geometry('450x80')

    l1 = Tkinter.Label(ask_rules, text="Régle de vie").grid(row = 0, column = 0)
    e1 = Tkinter.Entry(ask_rules)
    e1.grid(row = 0, column = 1)

    l2 = Tkinter.Label(ask_rules, text="Régle de mort").grid(row = 1, column = 0)
    e2 = Tkinter.Entry(ask_rules)
    e2.grid(row = 1, column = 1)

    Button(ask_rules, text='Fermer la fenêtre', command=ask_rules.destroy).grid(row=2, column= 1)
    Button(ask_rules, text="Règles par default", command = default_values).grid(row = 2, column = 2)
    Button(ask_rules, text="Changer les règles", command = change_values).grid(row = 2, column = 0)

    root.mainloop()
 # ------------------------------------------------------------------------------
 #changement des regles
def change_values():

    '''
    new_vie.set(e1.get())
    new_mort.set(e2.get())
    '''
    global new_vie, new_mort, vie, mort, ask_rules
    erreur = 0
    sum1 = -1
    sum2 = -1
    new_vie = e1.get()
    new_mort = e2.get()
    #gestion de l'erreur de saisi des nouvelles regles

    if len(new_vie)>9:
        new_vie = new_vie[:9]
    if len(new_mort)>9:
        new_mort = new_mort[:9]
    if len(new_vie)<9:
        new_vie = new_vie+(9-len(new_vie))*"0"
    if len(new_mort)<9:
        new_mort = new_mort+(9-len(new_mort))*"0"

    if(new_vie.isdigit() and new_mort.isdigit()):
        print("Good format")
    else:
        print("Bad format not digital")
        erreur=1
    if erreur == 0:
        vie = str(new_vie)
        mort = str(new_mort)
        print (str(vie)+"    "+ str(mort))
    else:
        attention = Tkinter.Toplevel(root)
        attention.title('Attention !')
        attention.geometry('250x30')
        at1 = Tkinter.Label(attention, text="On ne peut entrer que des 0 et des 1").grid(row = 1, column = 1)
        erreur = 0

# ------------------------------------------------------------------------------
#valeur par default des regles
def default_values():
    global new_vie, new_mort, vie, mort
    new_vie = '000100000'
    new_mort = '001100000'
    vie = str(new_vie)
    mort = str(new_mort)
    print (str(vie)+"    "+ str(mort))
# ==============================================================================
# ==============================================================================
global vie, mort, stop
vie = '000100000'
mort = '001100000'
cmmp=0
iteration=20
stop = 0
compteur = 1
#fenetre
root = Tk()
root.title('Jeu de la vie')
#taille de la fenetre
win_width = 500
win_height = 500
config_string = "{0}x{1}".format(win_width, win_height + 32)
#couleur des cellules vivantes
fill_color = "pink"
root.geometry(config_string)
cell_size = 20
canvas = Canvas(root, height = win_height)
canvas.pack(fill='both', expand = 'yes')

field_height = win_height // cell_size
field_width = win_width // cell_size

cell_matrix = []
cell_matrix_verif = []

for i in range(field_height):
    for j in range(field_width):
        square = canvas.create_rectangle(2 + cell_size * j, 2 + cell_size * i, cell_size + cell_size * j - 2, cell_size + cell_size * i - 2, fill = fill_color)
        canvas.itemconfig(square, state=HIDDEN, tags=('hid','0'))
        cell_matrix.append(square)
        cell_matrix_verif.append(square)
fict_square = canvas.create_rectangle(0,0,0,0, state=HIDDEN, tags=('hid','0'))
cell_matrix.append(fict_square)
cell_matrix_verif.append(fict_square)

#configuration de base a l'ouverture du programme
canvas.itemconfig(cell_matrix[addpoint(8, 8)], state=NORMAL, tags='vis')
canvas.itemconfig(cell_matrix[addpoint(10, 9)], state=NORMAL, tags='vis')
canvas.itemconfig(cell_matrix[addpoint(9, 9)], state=NORMAL, tags='vis')
canvas.itemconfig(cell_matrix[addpoint(9, 8)], state=NORMAL, tags='vis')
canvas.itemconfig(cell_matrix[addpoint(9, 7)], state=NORMAL, tags='vis')
canvas.itemconfig(cell_matrix[addpoint(10, 7)], state=NORMAL, tags='vis')
iii = 0
jjj = 0
for i in range(field_height):
    canvas.create_line(iii+20, 0, iii+20, 500)
    canvas.create_line(0, jjj+20, 500, jjj+20)
    iii+=20
    jjj+=20

frame = Frame(root)

#gestion des boutons
btn1 = Button(frame, text = 'Next generation', command = step)
btn2 = Button(frame, text = 'Clear', command = clear)
#btn3 = Button(frame, text = 'Planeur', command = planer)
#btn4 = Button(frame, text = 'Automatique', command = automatique)
btn5 = Button(frame, text = 'Demarer/Pause', command = pause)
btn6 = Button(frame, text = 'Open', command = file_to_open)
btn7 = Button(frame, text = 'Modification des regles', command = new_rules)


btn1.pack(side='left')
btn2.pack(side='left')
#btn3.pack(side='left')
#btn4.pack(side='left')
btn5.pack(side='left')
btn6.pack(side='left')
btn7.pack(side='left')


frame.pack(side='bottom', fill='x', expand = 'yes')

canvas.bind('<B1-Motion>', interpret)
canvas.bind('<ButtonPress>', interpret)

root.mainloop()
