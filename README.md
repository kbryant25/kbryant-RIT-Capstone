This is a repository for my senior capstone project N-Body Codes. 
> Abstract: The orbiting of a supermassive black hole binary system is a massively energetic phenomena that can have significant dynamical effects within active galactic nuclei (AGN). Eventually it is possible that these two supermassive black holes (SMBH) spiral into each other and collide, thus coalescing into a single larger SMBH. As a result of this collision and the emission of gravitational waves from the orbiting bodies, it is possible for the merged black hole to receive a “kick” velocity of up to several 1000 km/s and eject it from the center of its host galaxy. As the black hole leaves the AGN it drags some of the mass with it which changes the broad emission line signatures we would normally expect to receive from an AGN and allows us to detect the recoiling SMBH. In this project I will use an N-Body code to simulate the effect of the SMBH recoil on its surrounding galaxy. The simulation output will then make it possible to calculate the emission line profiles. Further analysis of these profiles will then help to identify characteristics of these recoil kicks and help guide the search for possible future candidates in spectroscopic databases. 

This code is based on the N-Body integrator code Rebound https://github.com/hannorein/rebound

You are free to use and modify this code however you like under the GNU General Public License v3.0. All I ask is that you credit myself as well as the creators of Rebound (And maybe send me any cool things you make I would love to see what other people do with this but it's up to you)

## Part 1: AGN-Body Code
This code will be used to simulate the broad line region surrounding the SMBH and what happens when the central mass recieves a kick velocity. Secondary codes  can also be created in order to show velocity mapping and bound orbits around the central mass.

- Strip AGN down into central mass surrounded by massless test particles
- Apply kick velocity to central mass
- Customizable parameters (SMBH mass, velocity, angle, range, AGN shape)

## Part 2: Data Extraction and Analysis (Clever code name pending)
Extract position and velocity vectors for each particle from the N-Body code and compile into a database. From there construct a code that is able to compute the line profiles from the database. From there spectroscopic analysis can be done on the emission lines created by the simulation.

- Extract position and velocity data from Rebound binary file
- Separate 6 variables by timestep
- Connect to BELPRO

## Part 3: Identify Trends in Profile Properties
Explore the parameter space: e.g., black hole mass, kick velocity, inclination, initial cloud distribution and velocity field etc. And identify trends in the profile properties (width, shift, asymmetry, kurtosis) that we are measuring from quasar spectra. The end goal is to compare these model parameters with measurements obtained from SDSS (Sloan Digital Sky Survey) spectra done by Emily Temple for her master’s thesis.

- Create database of output spectra from BELPRO
- Compare with SDSS spectra
