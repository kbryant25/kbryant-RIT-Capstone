# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:01:10 2024

@author: Karina Bryant
"""

import rebound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps


# Set Parameters --------------------------------------------------------------

BHM = 6.5*(10**9)    # Black hole mass
KV = 100        # Kick velocity in 2piAU/year = 29.7858905 km / s
dt = 0.05         # Timestep
RS = None        # Set seed for repeatability
Nimg = 200     # Number of frames (Note: when decreasing number make sure to delete images from animation file)
KVkms = KV * 29.7858905
print('Recoil velocity in km/s: ' + str(KVkms))

plt.ioff() #Tells spyder to only save the plots and not display them


# Simulation ------------------------------------------------------------------

"""Set up the particles in the simulation. Particles are added by default in
Jacobi coordinates (center-of-mass frame)"""

sim = rebound.Simulation()    # Initialize the simulation
sim.add(m = BHM)              # Add the central particle
np.random.seed(RS)            # Random seed for test cases


# Set up the test particles ---------------------------------------------------

N_testparticle = 1500         #Number of test particles
a_initial = np.linspace(130, 200, N_testparticle)
for a in a_initial:
    sim.add(a=a,f=np.random.rand()*2.*np.pi) # Mass is set to 0 by default, random true anomaly


# Save sim to binary file------------------------------------------------------

# sim.save_to_file('AGNBaseCode.bin')
""" Use to save to binary file, includes ALL information about the particles
(mass, position, velocity, etc), as well as the current simulation settings
such as time, integrator choice.
Only needs to be done once """


# Integration -----------------------------------------------------------------

for i in range(Nimg):
    if i == 0:
        # Print the base simulation before any modification
        coords = np.zeros((sim.N, 6))
        sim.serialize_particle_data(xyzvxvyvz=coords)
        fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2,2, figsize = (7,5.5), dpi = 200)

        ax1 = plt.subplot(2,2,3)
        ax1.set_facecolor('grey')
        vz = coords[:,5]
        plt.scatter(coords[:,0], coords[:,1], alpha = 0.25, s = 5)
        scatterxy = plt.scatter(coords[:,0], coords[:,1], c = vz, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatterxy)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        ax1.set_title("XY")

        ax2 = plt.subplot(2,2,4)
        vx = coords[:,3]
        plt.scatter(coords[:,2],coords[:,1], color = 'b', alpha = 0.25, s = 5)
        scatteryz = plt.scatter(coords[:,2], coords[:,1], c = vx, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatteryz)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.yticks(color='w')
        ax2.set_title("YZ")

        ax3 = plt.subplot(2,2,1)
        vy = coords[:,4]
        plt.scatter(coords[:,0],coords[:,2], color = 'b', alpha = 0.25, s = 5)
        scatterxz = plt.scatter(coords[:,0], coords[:,2], c = vy, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatterxz)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.xticks(color='w')
        ax3.set_title("XZ")

        ax4 = plt.subplot(2,2,2)
        plt.scatter(0,0, alpha = 0)
        plt.axis('off')
        plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)
        ax4.set_title("SMBH Recoil [Distance in AU]", fontsize = 10)
        sim.step()
    else:
        #Add velocity kick
        sim.move_to_hel()            # Move to the heliocentric reference frame
        sim.particles[0].vz = KV     # Changing the z velocity of the central particle to __ (in code units)
        sim.move_to_hel()            # Move into the new central particle-frame
        sim.dt = dt
        sim.step()
        coords = np.zeros((sim.N, 6))
        sim.serialize_particle_data(xyzvxvyvz=coords)
        fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2,2, figsize = (7,5.5), dpi = 200)

        ax1 = plt.subplot(2,2,3)
        vz = coords[:,5]
        plt.scatter(coords[:,0], coords[:,1], alpha = 0.25, s = 5)
        scatterxy = plt.scatter(coords[:,0], coords[:,1], c = vz, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatterxy)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        ax1.set_title("XY")

        ax2 = plt.subplot(2,2,4)
        vx = coords[:,3]
        plt.scatter(coords[:,2],coords[:,1], color = 'b', alpha = 0.25, s = 5)
        scatteryz = plt.scatter(coords[:,2], coords[:,1], c = vx, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatteryz)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.yticks(color='w')
        ax2.set_title("YZ")

        ax3 = plt.subplot(2,2,1)
        vy = coords[:,4]
        plt.scatter(coords[:,0],coords[:,2], color = 'b', alpha = 0.25, s = 5)
        scatterxz = plt.scatter(coords[:,0], coords[:,2], c = vy, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatterxz)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.xticks(color='w')
        ax3.set_title("XZ")

        ax4 = plt.subplot(2,2,2)
        plt.scatter(0,0, alpha = 0)
        plt.axis('off')
        plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)
        ax4.set_title("SMBH Recoil [Distance in AU]", fontsize = 10)
    # If you don't care about creating gifs and only want to create the simulation comment out the next line
    plt.savefig("path/image_%s.jpg" % i)
    sim.save_to_file("path/archive.bin")
    #Saving each plot to a file with it's own name to be created into a gif https://ezgif.com/maker
    plt.close()


# Print parameters for easy copy-pasting

# print('BH Mass: ' + str(BHM ))
# print('Number of test Particles: ' + str(N_testparticle))
# print('Kick velocity: '+ str(KV))
# print('Timestep: ' + str(dt))
# print('Random seed: ' + str(RS))
# print('Number of frames to generate: ' + str(Nimg))