# Script de tâche de pointage
# Auteur: Dorian Bannier
# Version: 03/01/2022

from psychopy import core, visual, gui, data, event
import random

expInfo = {'Nom':'Bond', 'Prénom du patient': 'James', 'nombrePointages':8}
expInfo['Date'] = data.getDateStr()  # add the current time
# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Paramètres de la tâche de pointage')
if not dlg.OK:
    core.quit()

# création de l'ordre des positions
position = []
position.append([-350,250])
position.append([350,250])
position.append([350,-250])
position.append([-350,-250])
position.append([0,0])

while len(position) < expInfo['nombrePointages']:
    position = position + position

random.shuffle(position)

# Pseudo-randomisation.
for i in range(len(position)):
    if i >= 1 and position[i] == position[i-1]:
        position.append(position.pop(i))

# On s'assure que le dernier élément est bien différent de l'avant-dernier (ce qui n'est pas le cas avec la boucle précédente).        
while position[-1] == position[-2]:
    position[-1] = random.choice(position)
        

position = position[0:expInfo['nombrePointages']]

# création de la fenêtre et du stimulus
win = visual.Window([800,600],allowGUI=True,
                    monitor='testMonitor', units='pix')
target = visual.Circle(win, fillColor = 'Red', radius = 30, units = 'pix')

# Affichage de l'acceuil
message = visual.TextStim(win, pos=[0,+3],text='Appuyer sur une touche pour commencer.')
message2 = visual.TextStim(win, pos=[0,-50], text = "Quitter: bouton q ou échap")
message.draw()
message2.draw()
win.flip()
event.waitKeys()

for i in range(len(position)):

    target.pos = position[i]
    target.draw()
    win.flip()
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey in ['q', 'escape']:
                win.close()
                core.quit()
            else:
                thisResp = -1
        event.clearEvents()
    
    win.flip()
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey in ['q', 'escape']:
                win.close()
                core.quit()
            else:
                thisResp = -1
        event.clearEvents()

message = visual.TextStim(win, text = "C'est terminé! Appuyer sur une touche pour quitter")
message.draw()
win.flip()
event.waitKeys()
win.close()
core.quit()
