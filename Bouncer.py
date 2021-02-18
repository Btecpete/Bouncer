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

#Creates possible v values
vs = []
for theta in thetas:
    h2 = math.sin(theta)
    vs.append(math.sqrt((10/7)*g*h2))

#Creates possible values of ux
uxs = []
for u in vs:
    for theta in thetas:
        uxs.append(u*math.cos(theta))

#Creates possible values of uy
uys = []
for u in vs:
    for theta in thetas:
        uys.append(u*math.sin(theta))

#Creates list of possible t1s
t1s = []
for vy in uys:
    for h in h2s:
        t = (-vy + math.sqrt((vy**2) - 4 * (g/2) * (-h)))/(2 * (g/2))
        t1s.append(t)

#Creates list of b1s
b1s = []
for t1 in t1s:
    for ux in uxs:
        b1s.append(t1*ux)

#Creates list of Vya, vy after 1st impact
vyas = []
for e in es:
    for uy in uys:
        for h2 in h2s:
            vyb = math.sqrt((uy**2) + 2 * g * h2)
            vyas.append(vyb * e)

#Creates a list of t2s
t2s = []
for vya in vyas:
    t2s.append(2 * (vya/g))

#Finally, creates list of Ds
Ds = []
for b1 in b1s:
    for t2 in t2s:
        for ux in uxs:
            b2 = t2 * ux
            D = b1 + b2
            Ds.append(D)

#Stores the actual number of possibilities:
num_Ds = len(Ds)
#This number is over 177,000. Plotting all of these is pointless

#Because we have so many D values, we will plot every 1000th one. This selects them.
new_Ds = Ds[1::1000]

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