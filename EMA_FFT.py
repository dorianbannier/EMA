# Version Tk - Pour EMG enregistré dans Synergy
############## Chargement des librairies ##########################################

import os
import sys
import numpy as np
import scipy.fftpack as syfp
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

############## Import et préparation des données ##################################

#Dossier où sont stockées les données
dossier="C:\\Users\\dorian.bannier\\Documents\\analyseEMA\\Source"
liste_fichiers=os.listdir(dossier)

#fréquence d'aquisition du système en s
freq= 0.000155

if  len(liste_fichiers) > 1 :
	date_recente = 0
	for i in range(0,len(liste_fichiers)) :
		date_fichier = os.path.getmtime(dossier+"\\"+liste_fichiers[i])
		if	date_recente < date_fichier :
			date_recente = date_fichier
			fichier = dossier+"\\"+liste_fichiers[i]
else :
	fichier = dossier+"\\"+liste_fichiers[0]

for i in range(0,len(liste_fichiers)) :
    if dossier+"\\"+liste_fichiers[i]!=fichier :
        os.remove(dossier+"\\"+liste_fichiers[i])


#Récupération et découpage des données
if fichier.endswith(".txt"):
        donnees=[]
        donnees_brutes=open(fichier).readlines()
        index = 0
        
        for i in range(0,len(donnees_brutes)):
            if donnees_brutes[i].find("longue(") != -1 :
                index = donnees_brutes[i].find("=")
                donnees.append(donnees_brutes[i][index+1:])                      
else :
        print("Pas de fichier de données")
        sys.exit()
Ncanal=len(donnees)


#Découpage des blocs de donnees en donnees individuelles
for i in range(0,Ncanal):
        donnees[i]=donnees[i].replace(',','.')
        donnees[i]=donnees[i].split(';')
        donnees[i] = [float(j) for j in donnees[i]]
if "Membres Sup" in donnees_brutes[2] :
        nom_canal=["Accel", "Biceps", "Flech Carpe", "Ext Carpe", "Ext Carpe Ct"]
elif "Membres Inf" in donnees_brutes[2] :
        nom_canal=["Accel", "Quad Hm", "Jamb Ant Hm", "Jamb Ext Hm", "Jamb Ant Cnt"]
else :
        nom_canal=["canal 1", "canal 2", "canal 3", "canal 4", "canal 5"]

################## Interface graphique ##############################
# Création et paramétrage de la fenêtre
app = tk.Tk() 
app.geometry("1740x820")
app.title("Analyse EMA")

# Définition des observateurs
debut = 0

# widgets
figure1 = Figure(figsize=(800/96,800/96), dpi = 96)
for i in range(0,Ncanal):
        N  = len(donnees[i])
        y = donnees[i]
        x = np.linspace(0, len(donnees[i])*freq , len(donnees[i]))
        position=int(str(Ncanal)+str(1)+str(i+1))
        ax = figure1.add_subplot(position)
        ax.plot(x, y)
        ax.set_xlabel('Temps')
        ax.set_ylabel(nom_canal[i])
        if i == 0 :
            ax.set_title('Domaine temporel')
graph = FigureCanvasTkAgg(figure1, app)
x = tk.Entry(app)
canvas = graph.get_tk_widget()
canvas.place(x = 10, y = 10)

parametresFrame = tk.Frame(app, width = 100, height = 800)
parametresFrame.place(x = 820, y = 10)

def fft(*args):
    figure2 = Figure(figsize=(800/96,800/96), dpi = 96)
    debut = var_debut.get()
    fin = var_fin.get()
    for i in range(0,Ncanal):
            N  = len(donnees[i][round(debut/freq):round(fin/freq)])
            yf = syfp.fft(np.asarray(donnees[i][round(debut/freq):round(fin/freq)]))
            xf = syfp.fftfreq(N,freq)
            index25Hz = np.where(np.trunc(xf) == 25)
            powerMax = np.argmax(yf[0:index25Hz[0][0]])
            freqPowerMax = xf[powerMax].round()
            position=int(str(Ncanal)+str(1)+str(i+1))
            ax = figure2.add_subplot(position)
            ax.plot(abs(xf),abs(yf)/N)
            mini, maxi = ax.get_ylim()
            ax.set_xlim((0,25))
            ax.set_xlabel('Fréquence')
            ax.set_ylabel(nom_canal[i])
            if i == 0 :
                ax.set_title('Domaine fréquentiel '+str(debut)+'  - ' +str(fin)+' s')

            if i != 0:
                ax.text(0.5,maxi - 0.2*maxi,"Pic de puissance à : " + str(freqPowerMax) + " Hz", fontsize = 9)
    graph = FigureCanvasTkAgg(figure2, app)
    canvas = graph.get_tk_widget()
    canvas.place(x = 950, y = 10)
    figure2.savefig('C:\\Users\\dorian.bannier\\Documents\\Test\\Cible\\Export-'+str(debut)+'-'+str(fin)+'s.png')
    

labelDebut = tk.Label(parametresFrame, text = "Début")
labelFin = tk.Label(parametresFrame, text = "Fin")

var_debut = tk.IntVar()
#var_debut.trace("w", definition_debut)
entryDebut = tk.Entry(parametresFrame, textvariable = var_debut)

var_fin = tk.IntVar()
#var_fin.trace("w", definition_fin)
entryFin = tk.Entry(parametresFrame, textvariable = var_fin)
boutonOk = tk.Button(parametresFrame, text = "Ok", height = 2, width = 5, command = fft, bg = "green")
boutonQuitter = tk.Button(parametresFrame, text = "Quitter", command = app.destroy, bg="red")
labelDebut.pack()
entryDebut.pack()
labelFin.pack()
entryFin.pack()
boutonOk.pack(ipadx = 20, pady = 20)
boutonQuitter.pack(ipadx = 20, pady = 10)

app.mainloop()
