# OpticalPumpingModel
Models the optical pumping of lithium 7 atoms by a polarized laser modulated by an AOM and two EOMs.
Created by Kevin Wen for Dr. Heinzen's research lab, Summer 2021



Files:

beam_spectrum.py - defines the specific laser frequencies we are using, and calculates the transition frequencies for Li 7 we are interested in. Taking the laser jitter into account, it calculates the average number of photons scattered per second for each transition. When ran, graphs the laser spectrum with the transition frequencies, and plots a few examples of scattering rate vs time for different transitions.

OP_graph_model.py - uses the state_data and the rates calculated from beam_spectrum to create and solve the rate equations associated with our optical pumping setup. When ran, plots the populations of the different spin states over time, and gives the pumping efficiency of our system after 1 cm of optical pumping.

Graphing_txt_resonator.py - defines a function for EOM laser modulation based on input power. When ran, graphs the strength of the side bands vs applied power to the resonator and EOM.

beam_class.py - creates classes and contains calculations for cross section and photon scattering rate. When ran, nothing happens.

state_data.py - contains data about the energy levels of the spin states and the relative strengths of the transitions. When ran, nothing happens.

7-28-2021_helicalTest_EOM_power.txt - data for the helical resonator
