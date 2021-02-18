# Solid Mechanics 1 - Bouncer Challenge
# Dyson School of Design Engineering 18/02/2021

#This program will graphically represent the effects of any uncertainty in the motion 
# of a projectile leaving a tube at a fixed height and angle.


import math
import numpy as np
import matplotlib.pyplot as plt

#Length of tube (in m)
l = 1

#Acceleration due to gravity
g = 9.81

#Angle of tube & uncertainty
theta = 36
theta_unc = 0.5

#Possible thetas, in radians
thetas = [(theta - theta_unc)*math.pi/180, (theta)*math.pi/180, (theta + theta_unc)*math.pi/180]

#Height of base of tube & uncertainty
h2 = 0.678
h2_unc = 0.0005

#Possible h2s
h2s = [h2 - h2_unc, h2, h2 + h2_unc]

#Coefficient of Restitution & uncertainty
e = 0.6557
e_unc = 0.02

#Possible es
es = [e - e_unc, e, e + e_unc]

#Initialise vectors (for definitions see diagram in main report)
vs = []     #All possible V
uxs = []    #All possible ux
uys = []    #All possible uy
t1s = []    #All possible t1
b1s = []    #All possible b1
vyas = []   #All possible Vy(after)s
t2s = []    #All possible t2
Ds = []     #All possible Ds


for theta in thetas:
    #Create possible h1 values, then v values from that
    h1 = math.sin(theta)
    v = math.sqrt((10/7)*g*h1)
    vs.append(v)

    #Create ux and uy values from corresponding thetas
    ux = v*math.cos(theta)
    uxs.append(ux)

    uy = v*math.sin(theta)
    uys.append(uy)

    #Step through possible h2s
    for h2 in h2s:
        #Create t1
        t1 = (-uy + math.sqrt((uy**2) - 4 * (g/2) * (-h2)))/(2 * (g/2))
        t1s.append(t1)
        #And hence create b1
        b1 = t1 * ux
        b1s.append(b1)
        
        #Step through possible es
        for e in es:
            #Create corresponding Vy(after)s
            vya = (math.sqrt((uy**2) + 2 * g * h2)) * e
            vyas.append(vya)

            #Create t2s
            t2 = 2 * (vya/g)
            t2s.append(t2)

            #Finally, create b2s ans thus Ds
            b2 = t2 * ux
            D = b1 + b2
            Ds.append(D)


#Stores the actual number of possibilities:
num_Ds = len(Ds)
#This number is over 177,000. Plotting all of these is pointless

#If any D values are to be excluded from the plot, slice Ds list here.
new_Ds = Ds

#Stores the plotted number of possibilities:
num_nDs = len(new_Ds)

#Creates an array of 1s to co-plot:
y = np.ones(len(new_Ds))

#Plots data
plt.figure().set_figwidth(15)
plt.scatter(new_Ds, y, s=0.5)
plt.title('Possible values for distance D with compounding uncertainty')
plt.xlabel('Distance D in metres')
plt.ylim(0.9, 1.1)
plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
plt.vlines(1.79917, 0, 2, colors='k', linestyles='dashed', linewidth=0.5)
plt.annotate('Calculated Value,\nD=1.799m', (1.79917+0.001, 0.95), size=7)
plt.legend([str(num_nDs) + ' points of ' + str(num_Ds) + ' possible points shown.'])
plt.savefig('Bouncer Uncertainty.png', dpi=300)
plt.show()

#Creates a table summarising inaccuracy
table = [
    ['Minumum Theta', round(min(thetas)/(math.pi/180), 3)],
    ['Maximum Theta', round(max(thetas)/(math.pi/180), 3)],
    ['Minumum h2', round(min(h2s)*100, 2)],
    ['Maximum h2', round(max(h2s)*100, 2)],
    ['Minumum D', round(min(Ds)*100, 2)],
    ['Mean D', round(np.mean(Ds)*100, 2)],
    ['Maximum D', round(max(Ds)*100, 2)],
    ['Accurate D', round(179.917, 1)],
    ['Standard Deviation of D', round(np.std(Ds), 3)]
]

table = plt.table(cellText=table, loc='center')
plt.axis('off')
table.scale(1, 2)
plt.savefig('Bouncer Table.png', dpi=300)
plt.show()