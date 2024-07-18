# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:01:49 2024

@author: Karina Bryant
"""

import rebound
import numpy as np
import matplotlib.pyplot as plt

# Set Parameters --------------------------------------------------------------

BHM = 6.5*(10**9)    # Black hole mass
KVZ = 50        # Kick velocity in 2piAU/year = 29.7858905 km / s
KVX = 100
KVY = 0
RS = None        # Set seed for repeatability
Nimg = 200     # Number of frames (Note: when decreasing number make sure to delete images from animation file)
KVZkms = KVZ * 29.7858905
KVXkms = KVX * 29.7858905
KVYkms = KVY * 29.7858905

print('Recoil z velocity in km/s: ' + str(KVZkms))
print('Recoil x velocity in km/s: ' + str(KVXkms))
print('Recoil y velocity in km/s: ' + str(KVYkms))


plt.ioff() #Tells spyder to only save the plots and not display them


# Simulation ------------------------------------------------------------------

"""Set up the particles in the simulation. Particles are added by default in
Jacobi coordinates (center-of-mass frame)"""

sim = rebound.Simulation()    # Initialize the simulation
sim.add(m = BHM)              # Add the central particle
np.random.seed(RS)            # Random seed for test cases


# Set up the test particles ---------------------------------------------------

N_testparticle = 1500         #Number of test particles
a_initial = np.linspace(100, 130, N_testparticle)    # Inner and outer radius
for a in a_initial:
    sim.add(a=a,f=np.random.rand()*2.*np.pi) # Mass is set to 0 by default, random true anomaly


# Integration -----------------------------------------------------------------

for i in range(Nimg):
    if i == 0:
        # Print the base simulation before any modification
        coords = np.zeros((sim.N, 6))
        sim.serialize_particle_data(xyzvxvyvz=coords)
        fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2,2, figsize = (8,8), dpi = 200)

        ax1 = plt.subplot(2,2,3)
        plt.scatter(coords[:,0],coords[:,1], color = 'k', alpha = 0.25, s = 10)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        ax1.set_title("XY")

        ax2 = plt.subplot(2,2,4)
        plt.scatter(coords[:,2],coords[:,1], color = 'b', alpha = 0.25, s = 10)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.yticks(color='w')
        ax2.set_title("YZ")

        ax3 = plt.subplot(2,2,1)
        plt.scatter(coords[:,0],coords[:,2], color = 'b', alpha = 0.25, s = 10)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.xticks(color='w')
        ax3.set_title("XZ")

        ax4 = plt.subplot(2,2,2)
        plt.scatter(0,0, alpha = 0)
        plt.axis('off')
        plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)
        ax4.set_title("SMBH Recoil [Distance in AU]\nInitial Z velocity (km/s): " + str(KVZkms)+"\nInitial X velocity (km/s): "+ str(KVXkms)+"\nInitial Y velocity (km/s): "+ str(KVYkms), fontsize = 13)
        sim.step()
    else:
        #Add velocity kick
        sim.move_to_hel()            # Move to the heliocentric reference frame
        sim.particles[0].vz = KVZ     # Changing the z velocity of the central particle to __ (in code units)
        sim.particles[0].vx = KVX
        sim.particles[0].vy = KVY
        sim.move_to_hel()            # Move into the new central particle-frame
        sim.step()
        coords = np.zeros((sim.N, 6))
        sim.serialize_particle_data(xyzvxvyvz=coords)
        fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2,2, figsize = (8,8), dpi = 200)

        ax1 = plt.subplot(2,2,3)
        plt.scatter(coords[:,0],coords[:,1], color = 'k', alpha = 0.25, s = 10)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        ax1.set_title("XY")

        ax2 = plt.subplot(2,2,4)
        plt.scatter(coords[:,2],coords[:,1], color = 'b', alpha = 0.25, s = 10)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.yticks(color='w')
        ax2.set_title("YZ")

        ax3 = plt.subplot(2,2,1)
        plt.scatter(coords[:,0],coords[:,2], color = 'b', alpha = 0.25, s = 10)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.xticks(color='w')
        ax3.set_title("XZ")

        ax4 = plt.subplot(2,2,2)
        plt.scatter(0,0, alpha = 0)
        plt.axis('off')
        plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)
        ax4.set_title("SMBH Recoil [Distance in AU]\nInitial Z velocity (km/s): " + str(KVZkms)+"\nInitial X velocity (km/s): "+ str(KVXkms)+"\nInitial Y velocity (km/s): "+ str(KVYkms), fontsize = 13)
    plt.savefig("path/image_%s.jpg" % i)
    sim.save_to_file("path/archive.bin")
    #Saving each plot to a file with it's own name to be created into a gif https://ezgif.com/maker
    plt.close()


# Print parameters for easy copy-pasting

print('BH Mass: ' + str(BHM ))
print('Number of test Particles: ' + str(N_testparticle))
print('Random seed: ' + str(RS))
print('Number of frames to generate: ' + str(Nimg))
