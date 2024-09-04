# -*- coding: utf-8 -*-
"""
Created on Tue Sep 3 12:05:46 2024

@author: Karina Bryant
"""

import rebound
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd


# Set Parameters --------------------------------------------------------------

BHM = 1.7*(10**8)             # Black hole mass
KVZ = 50                      # Kick velocity in 2piAU/year = 29.7858905 km / s
KVX = 0
KVY = 0
RS = None                     # Set seed for repeatability
N_testparticle = 1500         #Number of test particles
Nimg = 10                     # Number of frames 
# (Note: when decreasing number make sure to delete images from animation file)
KVZkms = KVZ * 29.7858905
KVXkms = KVX * 29.7858905
KVYkms = KVY * 29.7858905


plt.ioff() #Tells IDE to only save the plots and not display them for speed

# Simulation ------------------------------------------------------------------

"""Set up the particles in the simulation. Particles are added by default in
Jacobi coordinates (center-of-mass frame)"""

sim = rebound.Simulation()    # Initialize the simulation
sim.add(m = BHM)              # Add the central particle
np.random.seed(RS)            # Random seed for test cases


# Set up the test particles ---------------------------------------------------

a_initial = np.linspace(3.3, 8, N_testparticle) # Initial range of semi major axis to distribute particles
for a in a_initial:
    sim.add(a=a,f=np.random.rand()*2.*np.pi)    # Mass is set to 0 by default, random true anomaly


# Print parameters for easy copy-pasting---------------------------------------

print('Recoil z velocity in km/s: ' + str(KVZkms))
print('Recoil x velocity in km/s: ' + str(KVXkms))
print('Recoil y velocity in km/s: ' + str(KVYkms))
print('BH Mass: ' + str(BHM ))
print('Number of test Particles: ' + str(N_testparticle))
print('Random seed: ' + str(RS))
print('Number of frames to generate: ' + str(Nimg))


# Integration -----------------------------------------------------------------

for i in range(Nimg):
    if i == 0:
        # Print the base simulation before any modification
        coords = np.zeros((sim.N, 6))
        sim.serialize_particle_data(xyzvxvyvz=coords)
        fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2,2, figsize = (9,8), dpi = 200)

        # XY graph
        ax1 = plt.subplot(2,2,3)
        ax1.set_facecolor('grey')
        vz = coords[:,5]
        plt.scatter(coords[:,0], coords[:,1], alpha = 0.25, s = 5)
        scatterxy = plt.scatter(coords[:,0], coords[:,1], c = vz, cmap = 'coolwarm_r', s = 5)
        plt.colorbar(scatterxy)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        ax1.set_title("XY")

        # YZ graph
        ax2 = plt.subplot(2,2,4)
        vx = coords[:,3]
        plt.scatter(coords[:,2],coords[:,1], color = 'b', alpha = 0.25, s = 5)
        scatteryz = plt.scatter(coords[:,2], coords[:,1], c = vx, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatteryz)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.yticks(color='w')
        ax2.set_title("YZ")

        # XZ graph
        ax3 = plt.subplot(2,2,1)
        vy = coords[:,4]
        plt.scatter(coords[:,0],coords[:,2], color = 'b', alpha = 0.25, s = 5)
        scatterxz = plt.scatter(coords[:,0], coords[:,2], c = vy, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatterxz)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.xticks(color='w')
        ax3.set_title("XZ")

        # Empty space
        ax4 = plt.subplot(2,2,2)
        plt.scatter(0,0, alpha = 0)
        plt.axis('off')
        plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)
        ax4.set_title("SMBH Recoil [Distance in AU]\nInitial Z velocity (km/s): " + str(KVZkms)+"\nInitial X velocity (km/s): "+ str(KVXkms)+"\nInitial Y velocity (km/s): "+ str(KVYkms), fontsize = 13)
        sim.step()
   
    else:
        #Add velocity kick
        sim.move_to_hel()             # Move to the heliocentric reference frame
        sim.particles[0].vz = KVZ     # Changing the z velocity of the central particle to __ (in code units)
        sim.particles[0].vx = KVX
        sim.particles[0].vy = KVY        
        sim.move_to_hel()             # Move into the new central particle-frame
        sim.step()
        coords = np.zeros((sim.N, 6))
        sim.serialize_particle_data(xyzvxvyvz=coords)
        fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2,2, figsize = (9,8), dpi = 200)

        # XY graph
        ax1 = plt.subplot(2,2,3)
        vz = coords[:,5]
        plt.scatter(coords[:,0], coords[:,1], alpha = 0.25, s = 5)
        scatterxy = plt.scatter(coords[:,0], coords[:,1], c = vz, cmap = 'coolwarm_r', s = 5)
        plt.colorbar(scatterxy)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        ax1.set_title("XY")

        # YZ graph
        ax2 = plt.subplot(2,2,4)
        vx = coords[:,3]
        plt.scatter(coords[:,2],coords[:,1], color = 'b', alpha = 0.25, s = 5)
        scatteryz = plt.scatter(coords[:,2], coords[:,1], c = vx, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatteryz)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.yticks(color='w')
        ax2.set_title("YZ")

        # XZ graph
        ax3 = plt.subplot(2,2,1)
        vy = coords[:,4]
        plt.scatter(coords[:,0],coords[:,2], color = 'b', alpha = 0.25, s = 5)
        scatterxz = plt.scatter(coords[:,0], coords[:,2], c = vy, cmap = 'coolwarm', s = 5)
        plt.colorbar(scatterxz)
        plt.scatter(0,0, marker = '*', color = 'm', s = 75)
        plt.xticks(color='w')
        ax3.set_title("XZ")

        # Empty space
        ax4 = plt.subplot(2,2,2)
        plt.scatter(0,0, alpha = 0)
        plt.axis('off')
        plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)
        ax4.set_title("SMBH Recoil [Distance in AU]\nInitial Z velocity (km/s): " + str(KVZkms)+"\nInitial X velocity (km/s): "+ str(KVXkms)+"\nInitial Y velocity (km/s): "+ str(KVYkms), fontsize = 13)
    
    # If you don't care about creating animations and only want to create the simulation comment out the next line
    plt.savefig("path/image_%s.jpg" % i)
    # Save to binary file so it doesn't lose precision
    sim.save_to_file("path/archive.bin") 
    #Saving each plot to a file with it's own name to be created into a gif https://ezgif.com/maker
    plt.close()


#%% Begin Data Extraction

# Removes previous files so the data is replaced if needed---------------------

os.remove('path/simXdata.csv')
os.remove('path/simYdata.csv')
os.remove('path/simZdata.csv')
os.remove('path/simVXdata.csv')
os.remove('path/simVYdata.csv')
os.remove('path/simVZdata.csv')
os.remove('path/THE.csv')


#%%
# Initialize Simulationarchive simulation--------------------------------------

sa = rebound.Simulationarchive("path/archive.bin")
N_archives = len(sa)


# Initialize empty data arrays-------------------------------------------------

save_times = np.zeros(N_archives)
# 2 dimensional array of size N saves and M particles
particles_x = np.zeros((N_archives, (N_testparticle + 1))) 
particles_y = np.zeros((N_archives, (N_testparticle + 1)))
particles_z = np.zeros((N_archives, (N_testparticle + 1)))
particles_vx = np.zeros((N_archives, (N_testparticle + 1)))
particles_vy = np.zeros((N_archives, (N_testparticle + 1)))
particles_vz = np.zeros((N_archives, (N_testparticle + 1)))


# Now loop through the saves and pull out all of the values of interest--------

for i, sim in enumerate(sa):
    save_times[i] = sim.t
    for j in range(1, sim.N):
        particles_x[i, j] = sim.particles[j].x
        particles_y[i, j] = sim.particles[j].y
        particles_z[i, j] = sim.particles[j].z
        particles_vx[i, j] = sim.particles[j].vx
        particles_vy[i, j] = sim.particles[j].vy
        particles_vz[i, j] = sim.particles[j].vz


# Save each individual parameter to its own CSV--------------------------------

x_data = np.concatenate([[save_times], particles_x.T])
np.savetxt('path/simXdata.csv', x_data, delimiter=', ')

vx_data = np.concatenate([[save_times], particles_vx.T])
np.savetxt('path/simVXdata.csv', vx_data, delimiter=', ')

y_data = np.concatenate([[save_times], particles_y.T])
np.savetxt('path/simYdata.csv', y_data, delimiter=', ')

vy_data = np.concatenate([[save_times], particles_vy.T])
np.savetxt('path/simVYdata.csv', vy_data, delimiter=', ')

z_data = np.concatenate([[save_times], particles_z.T])
np.savetxt('path/simZdata.csv', z_data, delimiter=', ')

vz_data = np.concatenate([[save_times], particles_vz.T])
np.savetxt('path/simVZdata.csv', vz_data, delimiter=', ')


# Read CSV files into dataframes-----------------------------------------------

x = pd.read_csv('path/simXdata.csv')
y = pd.read_csv('path/simYdata.csv')
z = pd.read_csv('path/simZdata.csv')
vx = pd.read_csv('path/simVXdata.csv')
vy = pd.read_csv('path/simVYdata.csv')
vz = pd.read_csv('path/simVZdata.csv')


#%%
# Split CSVs into individual timestep CSVs-------------------------------------

var_list = ['X', 'Y', 'Z', 'Vx', 'Vy', 'Vz'] # Column titles
t_step = np.arange(Nimg)                     # Number of files it needs to make - Matches with # of images
df_list = [x, y, z, vx, vy, vz]              # List of dataframes
t_dict = {}
for i, t in enumerate(t_step):               # Loop through each column in each parameter csv
    temp_df = pd.DataFrame()
    for j, df in enumerate(df_list):
        var = var_list[j]
        temp_df[var] = df.iloc[1:, i]
    # Save each timestep to separate CSV
    temp_df.to_csv(f'path/TimestepData/t{t}.csv')
    

#%%
# One big CSV------------------------------------------------------------------

"""
NOTE: Rebound begins indexing particles at 0. The csv indexes starting at 1. In
this csv, the timestep label is index 0

NOTE 2: In theorey you shouldn't need to combine all of this data into one big 
file but the option is here if you want

NOTE 3: This is cursed I know but we're trying to put a hypercube into a 2D
CSV file it's cursed by definition
"""

data = [x,y,z,vx,vy,vz]
columns = ['x','y','z','vx','vy','vz']

pieces = {"x": x, "y": y, "z": z, "vx": vx, "vy": vy, "vz": vz}

df = pd.concat(pieces, axis = 1)
df = df.rename(columns ={0:'Parameter'})
df.to_csv('path/THE.csv', header = True )

new_df = df.dropna(inplace = True) # Skips any particles that leave sim scope

"""***************************************************************************
IMPORTANT
PLEASE DON'T OPEN THIS CSV FILE ONCE IT GETS TOO BIG, OPENING IT *WILL* CRASH 
YOUR COMPUTER
Source: Just trust me...
"""





