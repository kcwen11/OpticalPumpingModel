import matplotlib.pyplot as plt
import numpy as np
import Graphing_txt_resonator as Mod
band_strength = Mod.band_strength

# this module defines the class for the laser modulation

##########################################################################################################
# constants
gamma = 5.9 * 10 ** 6  # Hz, rate of spontaneous emission
A21 = 3.7 * 10 ** 7  # Hz, Einstein A Coefficient for our lithium transitions
res_cross_sect = 2.1433 * 10 ** -13  # m ** 2, resonant cross section
h_bar = 1.055 * 10 ** -34  # J * s, reduced planck's constant
##########################################################################################################


# the lowest level is a Band, which is a single peak with a power and a frequency. all the plotting and calculations
# is based off the Band. all other classes only exist to create Bands.
class Band:
    def __init__(self, power, freq):
        self.power = power
        self.freq = freq

    def cross_sect(self, freq_0):  # does not take cross section relative strength into account. that happens later
        # freq_0 is the frequency of any transition, while self.freq is the frequency of the Band which does not change
        # if you want a laser with a different frequency you need to define a new Band or Beam
        if np.abs(freq_0 - self.freq) > 100 * 10 ** 6:
            return 0
        else:
            delta_omega = (self.freq - freq_0)
            return res_cross_sect * (gamma / 2) ** 2 / (delta_omega ** 2 + (gamma / 2) ** 2)

    def transition_rate(self, freq_0):  # gives the photon scattering rate for a single transition frequency freq_0
        # based on the frequency and intensity of the laser band, as well as the cross section
        rate3 = self.power * self.cross_sect(freq_0) / (h_bar * 2 * np.pi * freq_0)
        if rate3 > A21:
            return A21
        else:
            return rate3

    def plot(self, main_freq):  # plots a line showing the frequency of the Band relative to main_freq
        plt.plot([self.freq - main_freq, self.freq - main_freq], [self.power, 0], 'k')


# the middle level is the 800MHz modulation, which splits the main Beam into three smaller bands
# each of these Band800s will be split into five smaller Bands based on the dBm applied to the resonator + EOM
class Band800:
    def __init__(self, power, freq, dBm80):
        self.power = power
        self.freq = freq
        self.spectrum1 = []
        self.spectrum1.append(Band(power * band_strength(dBm80, 3), freq - 160 * 10 ** 6))
        self.spectrum1.append(Band(power * band_strength(dBm80, 2), freq - 80 * 10 ** 6))
        self.spectrum1.append(Band(power * band_strength(dBm80, 1), freq))
        self.spectrum1.append(Band(power * band_strength(dBm80, 2), freq + 80 * 10 ** 6))
        self.spectrum1.append(Band(power * band_strength(dBm80, 3), freq + 160 * 10 ** 6))

    def transition_rate(self, freq_0):
        rate1 = 0
        for i in self.spectrum1:
            rate1 = rate1 + i.transition_rate(freq_0)
        return rate1

    def plot(self, main_freq):
        for i in self.spectrum1:
            i.plot(main_freq)


# the highest level is the Beam. this is the laser before any modulation (not including the lone 201 MHz band created
# by the AOM - that one is defined as a separate Band)
class Beam:
    def __init__(self, power, freq, mod800, dBm80):
        self.power = power
        self.freq = freq
        self.spectrum0 = []
        self.spectrum0.append(Band800(self.power * mod800, freq - 800 * 10 ** 6, dBm80))
        self.spectrum0.append(Band800(self.power * (1 - mod800 * 2), freq, dBm80))
        self.spectrum0.append(Band800(self.power * mod800, freq + 800 * 10 ** 6, dBm80))

    def transition_rate(self, freq_0):
        rate0 = 0
        for i in self.spectrum0:
            rate0 = rate0 + i.transition_rate(freq_0)
        return rate0

    def plot(self, main_freq):
        for i in self.spectrum0:
            i.plot(main_freq)
