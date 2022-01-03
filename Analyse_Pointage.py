from ezc3d import c3d
import numpy as np
import math
import matplotlib.pyplot as plt

# Import des données
data = c3d('Test01.c3d')
point_data = data['data']['points']
mires = data['parameters']['POINT']['LABELS']['value']
analog_data = data['data']['analogs']
emg = data['parameters']['ANALOG']['LABELS']['value']
emg = emg[12:16]
emg_data = analog_data[0,12:16,:]

# Calcul des distances du doigt au plan
distance = []
for i in range(point_data.shape[2]):
    Pt1 = np.array([point_data[0, 0, i], point_data[1, 0, i], point_data[2, 0, i]]) #LHEE
    Pt2 = np.array([point_data[0, 1, i], point_data[1, 1, i], point_data[2, 1, i]]) # LANK
    Pt3 = np.array([point_data[0, 3, i], point_data[1, 3, i], point_data[2, 3, i]]) # LFOO
    
    v1 = Pt3 - Pt1
    v2 = Pt2 - Pt1
    
    cp = np.cross(v1,v2)
    a, b, c = cp
    
    d = np.dot(cp, Pt3)
    
    x1 = point_data[0, 4, i]
    y1 = point_data[1, 4, i]
    z1 = point_data[2, 4, i]
    
    e = abs((a * x1 + b * y1 + c * z1 - d))
    f = (math.sqrt(a * a + b * b + c * c))

    distance.append(e/f)

# Création des triggers (variable t)
trigger = []
somme = 0
for i in range(len(distance)-1):
    if i <= 1:
        trigger.append(0)
    elif abs(distance[i+1]-distance[i]) < 1 and distance[i] < 10:
        trigger.append(somme+1)
        somme = somme + 1
    else:
        trigger.append(0)
        somme = 0

t = [i for i in range(len(trigger)) if trigger[i]  == 1]

# Création des epochs
x = []
emg_epoched = []
for i in range(emg_data.shape[0]):
    for j in t:
        x.append(emg_data[i, (j-100)*10:(j+10)*10])

a = 0
b = len(t)
for i in range(emg_data.shape[0]):
    emg_epoched.append(x[a:b])
    a = b
    b = b+len(t)

# Création des EMG évoqués
emg_evoked = []
for i in emg_epoched:
    emg_evoked.append(np.mean(i, axis = 0))

x = range(-1000, 100, 1)
muscles = ['Muscle1', "Muscle2", 'Muscle3', 'Muscle4']

fig = plt.figure(figsize = (10,10))

for i in range(len(emg_evoked)):
    plt.subplot(len(emg_evoked), 1, i+1)
    plt.plot(x, emg_evoked[i])
    plt.grid(linestyle=':')
    plt.ylabel(muscles[i])
    plt.axhline(y = 0, c = '0.5')
    plt.axvline(x = 0, c = '0.5')
    if i == len(emg_evoked)-1:
        plt.xlabel('Temps (en ms)')
    
plt.savefig('test.png', dpi=300)

############### Comparaison à une baseline (début de l'enregistrement)
emg_baseline = emg_data[0:4, 0:1000]
emg_base_moyenne = np.mean(abs(emg_baseline), axis = 1)
emg_evoked_abs = [abs(i) for i in emg_evoked]
emg_cond_moyenne = np.mean(emg_evoked_abs, axis = 1)
emg_moyenne = [emg_base_moyenne, emg_cond_moyenne]

# The x position of bars
barWidth = 0.3
r1 = np.arange(len(emg_cond_moyenne))
r2 = [x + barWidth for x in r1]

fig = plt.figure(figsize = (7,5))
plt.bar(r1, emg_base_moyenne, width = barWidth, color = 'crimson', label = "Contrôle")
plt.bar(r2, emg_cond_moyenne, width = barWidth, color = 'darkcyan', label = "Pointage")
plt.xticks([r + barWidth/2  for r in range(len(emg_base_moyenne))], muscles)
plt.ylabel('Amplitude moyenne (en µV)')
plt.legend()
plt.axhline(y = 0, c = '0.5')
plt.savefig('test2.png', dpi = 300)