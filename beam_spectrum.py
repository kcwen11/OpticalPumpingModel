import matplotlib.pyplot as plt
import numpy as np
import copy
import beam_class
import state_data
Beam = beam_class.Beam
Band = beam_class.Band
abs_str = state_data.abs_str

# this is the frequency of the laser without modulation
main_freq = 4.475 * 10 ** 14 + 803 * 10 ** 6  # Hz, the B=0, F_g=1 -> F_e=2 transition

beam_power = 80  # total power of laser, split into many side bands
lone_power = 20  # power of the lone band going out of the AOM, +201 MHz off the main
mod800 = 0.30  # percent of power in the 800 MHz sidebands
dBm80 = -14  # power of the rf source, going into the resonator (see Graphing_txt_resonator for ratios)
polar_frac = 98 / 100  # fraction of the laser in the correct +sigma polarization
# (we assume the incorrect polarization is split evenly with -sigma and pi)

main_OP_beam = Beam(beam_power, main_freq, mod800, dBm80)
lone_band = Band(lone_power, main_freq + 201 * 10 ** 6)

energy_g = state_data.energy_g  # in MHz, for ground states it is relative to the B = 0, F_g = 1 energy
energy_e = state_data.energy_e  # in MHz, for excited states it is relative to the B = 0, F_e = 2 energy
delta_freq = copy.deepcopy(state_data.allowed_transitions)  # MHz relative to the B=0, F_g=1 -> F_e=2 transition
for g_state, e_dict in delta_freq.items():
    for e_state, zero in e_dict.items():
        delta_freq[g_state][e_state] = energy_e[e_state] - energy_g[g_state]
# {delta_freq} gives the resonant frequency for each possible transition

main_transitions = [('|1, 1)', 'e|2, 2)'), ('|1,-1)', 'e|2, 0)'), ('|1, 0)', 'e|1, 1)'), ('|2,-2)', 'e|1,-1)'),
                    ('|2,-1)', 'e|2, 0)'), ('|2, 0)', 'e|2, 1)'), ('|2, 1)', 'e|2, 2)'), ('|2,-1)', 'e|1, 0)'),
                    ('|2, 2)', 'e|2, 1)'), ('|2, 2)', 'e|1, 1)')
                    ]  # for the purpose of graphing the main transitions on the spectrum

# the laser is not at a constant frequency, so we cannot treat the transitions as always on resonance.
# we can model the laser jitter as a sine wave and use that to find the transition rate over one period
jitter_freq = 800000
time = np.arange(0, 1 / jitter_freq, 1 / jitter_freq / 125)  # one period of the laser jitter
jitter = 20 * 10 ** 6 * np.sin(2 * np.pi * jitter_freq * time)  # the laser jitter over one period

beam_jitter_main = []
beam_jitter_lone = []
for i in jitter:
    beam_jitter_main.append(Beam(beam_power, main_freq + i, mod800, dBm80))
    beam_jitter_lone.append(Band(lone_power, main_freq + i + 201 * 10 ** 6))
# a list of different laser spectra at different times during the jitter (different main frequencies)


def rate_jitter(freq):  # calculates the transition rate at each time during the beam jitter
    rate_list = []
    for j in range(len(beam_jitter_main)):
        rate_list.append(beam_jitter_main[j].transition_rate(freq) + beam_jitter_lone[j].transition_rate(freq))
    return rate_list


if __name__ == '__main__':
    # plots the spectrum and transitions
    plt.title('Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Intensity')
    main_OP_beam.plot(main_freq)
    lone_band.plot(main_freq)
    plt.show()

    plt.title('Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Intensity')
    main_OP_beam.plot(main_freq)
    lone_band.plot(main_freq)
    offset = 0
    for k, l in main_transitions:
        if float(k[3:5]) < float(l[4:6]):
            plt.annotate(k + '->' + l, xy=(delta_freq[k][l] * 10 ** 6, 0), xytext=(0, 50 + offset),
                         textcoords='offset points', arrowprops=dict(facecolor='green', shrink=0.05),
                         color='green', weight='extra bold')
            offset = offset + 15
        else:
            plt.annotate(k + '->' + l, xy=(delta_freq[k][l] * 10 ** 6, 0), xytext=(0, 50 + offset),
                         textcoords='offset points', arrowprops=dict(facecolor='red', shrink=0.05),
                         color='red', weight='extra bold')
            offset = offset + 15

    plt.show()

    plt.title('Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Intensity')
    main_OP_beam.plot(main_freq)
    lone_band.plot(main_freq)
    offset = 0
    for k, l in delta_freq.items():
        for m, n in l.items():
            if float(k[3:5]) < float(m[4:6]):
                plt.annotate(k + '->' + m, xy=(n * 10 ** 6, 0), xytext=(0, 80 - n / 6), textcoords='offset points',
                             arrowprops=dict(facecolor='green', shrink=0.05), color='green', weight='extra bold')
                offset = offset + 5
    plt.show()

    plt.title('Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Intensity')
    main_OP_beam.plot(main_freq)
    lone_band.plot(main_freq)
    offset = 0
    for k, l in delta_freq.items():
        for m, n in l.items():
            if not (float(k[3:5]) < float(m[4:6])):
                plt.annotate(k + '->' + m, xy=(n * 10 ** 6, 0), xytext=(0, 80 - n / 6), textcoords='offset points',
                             arrowprops=dict(facecolor='red', shrink=0.05), color='red', weight='extra bold')
                offset = offset + 5
    plt.show()

    # plots the laser jitter over one period
    plt.title('Jitter')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.plot(time, jitter, 'k')
    plt.show()

    # plots the rate of two transitions over one period of laser jitter
    n_64_jitter = rate_jitter(main_freq - 64 * 10 ** 6 - 800 * 10 ** 6)
    plt.title('[2, 1)->e[2, 2) Good Transition at -64-800 MHz')
    plt.xlabel('Time (s)')
    plt.ylabel('Rate (photons / s * atom) before reducing resonant cross section')
    plt.plot(time, n_64_jitter, 'k')
    print('number of photons scattered by [2, 1)->e[2, 2) transition before reducing resonant cross section',
          np.trapz(n_64_jitter, x=time) * jitter_freq / 20000)
    # integrates rate vs time to get number of photons scattered in one period. I multiply it by jitter_freq/20000 to
    # get the number of photons scattered in the 1 cm beam (the atoms are moving at 20000 cm/s)

    # this is meant to be a demonstration of how I find the average rate for each transition. later in the code, I
    # calculate this integral for every transition
    plt.show()

    n_150_jitter = rate_jitter(main_freq - 150 * 10 ** 6 - 800 * 10 ** 6)
    plt.title('[2, 2)->e[2, 1)  Bad Transition at -150-800 MHz')
    plt.xlabel('Time (s)')
    plt.ylabel('Rate (photons / (s * atom) before reducing resonant cross section')
    plt.plot(time, n_150_jitter, 'k')
    print('number of photons scattered by [2, 2)->e[2, 1) transition '
          '(without considering polar and cross section reduction)',
          np.trapz(n_150_jitter, x=time) * jitter_freq / 20000)
    plt.show()

num_photons = copy.deepcopy(state_data.allowed_transitions)  # number of photons absorbed in 1 cm, at 20000 cm/s
rates = copy.deepcopy(state_data.allowed_transitions)  # number of photons absorbed per second per atom

for g_state, e_dict in delta_freq.items():
    for e_state, t_freq in e_dict.items():
        # for every transition, integrates rate vs time for one period
        # multiplying it by the number of periods of laser jitter in 1 cm gives the total number of photons scattered
        # by a transition in the 1 cm beam
        num = np.trapz(rate_jitter(main_freq + t_freq * 10 ** 6), x=time) * jitter_freq / 20000
        if float(g_state[3:5]) < float(e_state[4:6]):  # for +sigma polarized light
            num_photons[g_state][e_state] = num * polar_frac * abs_str[g_state][e_state]
            # above, I correct for the reduction of maximum cross section due to the relative strengths of the
            # transitions. also, I account for the photons lost due to being in the wrong polarization for the
            # transition
            rates[g_state][e_state] = num * polar_frac * abs_str[g_state][e_state] * 20000
            # I have the number of photons scattered in 1 cm of the beam, so by multiplying it by 20000 cm/s, I can
            # get the average transition rate. this will be used in the differential equations
        elif float(g_state[3:5]) == float(e_state[4:6]):  # for pi polarized light, res cross section is halved
            num_photons[g_state][e_state] = num * ((1 - polar_frac) / 2) * abs_str[g_state][e_state] / 2
            rates[g_state][e_state] = num * ((1 - polar_frac) / 2) * abs_str[g_state][e_state] * 20000 / 2
        else:  # for -sigma polarized light
            num_photons[g_state][e_state] = num * ((1 - polar_frac) / 2) * abs_str[g_state][e_state]
            rates[g_state][e_state] = num * ((1 - polar_frac) / 2) * abs_str[g_state][e_state] * 20000
            # I assume both types of incorrect polarization have the same population

print('###############################################################################################################')
print('the number of photons scattered by each transition over 1 cm of optical pumping, with polarization')
print(num_photons)
