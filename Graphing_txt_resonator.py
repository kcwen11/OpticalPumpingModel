import matplotlib.pyplot as plt
import numpy as np

# this is the data we got from testing the helical resonator. there is more info in the notebook
# I use the data to model the laser beam in the module beam_class
txtfile = open("7-28-2021_helicalTest_EOM_power.txt", "r")
txtdata = []

skip = 0
for i in txtfile:
    plaintext = i.strip()
    plainvalues = plaintext.split()
    for k in range(len(plainvalues)):
        try:
            plainvalues[k] = float(plainvalues[k])
        except ValueError:
            skip = 1
    if skip == 0:
        txtdata.append(plainvalues)
    else:
        skip = 0

txtfile.close()

data = np.array(txtdata)
dBm, main, side, second_ord, third_ord, v_ref = zip(*data)
plot_vars = [dBm, main, side, second_ord, third_ord, v_ref]
for i in range(len(plot_vars)):
    plot_vars[i] = np.asarray(plot_vars[i])

allpeaks = plot_vars[1] + 2 * (plot_vars[2] + plot_vars[3] + plot_vars[4])


# for a given dBm of the rf source, this function outputs the power in each side band divided by the total power.
# it is based on the data. I use this in the beam_class module
def band_strength(in_dBm, band):
    l_index = np.where(plot_vars[0] <= in_dBm)[0][-1]
    l_dist = in_dBm - plot_vars[0][l_index]
    t_dist = plot_vars[0][l_index + 1] - plot_vars[0][l_index]
    amp_dist = (plot_vars[band] / allpeaks)[l_index + 1] - (plot_vars[band] / allpeaks)[l_index]
    return (plot_vars[band] / allpeaks)[l_index] + amp_dist * l_dist / t_dist


if __name__ == '__main__':
    plt.plot(plot_vars[0], plot_vars[1], label='Main', marker='o')
    plt.plot(plot_vars[0], plot_vars[2], label='Side Band', marker='o')
    plt.plot(plot_vars[0], plot_vars[3], label='Second Order', marker='o')
    plt.plot(plot_vars[0], plot_vars[4], label='Third Order', marker='o')

    plt.title("Peak Strength vs Power Applied to Resonator")
    plt.xlabel("Power (dBm)")
    plt.ylabel("Peak Strength (mV)")

    plt.legend()
    plt.tick_params(axis='both', direction='in', top='true', right='true')
    plt.show()

    # I use this to show the total power is more or less constant, just checking if I made any mistakes
    plt.plot(dBm, allpeaks, label='All Peaks')

    plt.title("Peak Strength vs Power Applied to Resonator")
    plt.xlabel("Power (dBm)")
    plt.ylabel("Peak Strength (mV)")

    plt.legend()
    plt.tick_params(axis='both', direction='in', top='true', right='true')
    plt.show()

    # the ratio of amplitude in each peak to the total amplitude
    plt.plot(plot_vars[0], plot_vars[1] / allpeaks, label='Main', marker='o')
    plt.plot(plot_vars[0], plot_vars[2] / allpeaks, label='Side Band', marker='o')
    plt.plot(plot_vars[0], plot_vars[3] / allpeaks, label='Second Order', marker='o')
    plt.plot(plot_vars[0], plot_vars[4] / allpeaks, label='Third Order', marker='o')

    plt.title("Peak Strength Ratio vs Power Applied to Resonator")
    plt.xlabel("Power (dBm)")
    plt.ylabel("Peak Strength / Total Strength")

    plt.legend()
    plt.tick_params(axis='both', direction='in', top='true', right='true')
    plt.show()

    # the ratio of amplitude in each peak to the main peak
    plt.plot(plot_vars[0], plot_vars[1] / plot_vars[1], label='Main', marker='o')
    plt.plot(plot_vars[0], plot_vars[2] / plot_vars[1], label='Side Band', marker='o')
    plt.plot(plot_vars[0], plot_vars[3] / plot_vars[1], label='Second Order', marker='o')
    plt.plot(plot_vars[0], plot_vars[4] / plot_vars[1], label='Third Order', marker='o')

    plt.title("Peak Strength Ratio vs Power Applied to Resonator")
    plt.xlabel("Power (dBm)")
    plt.ylabel("Peak Strength / Main Peak")

    plt.legend()
    plt.tick_params(axis='both', direction='in', top='true', right='true')
    plt.show()

    # the reflected voltage measured by the directional coupler and the oscilloscope
    plt.plot(plot_vars[0], plot_vars[5], label='Reflected Voltage', marker='o')

    plt.title("Reflected Voltage vs Power Applied to Resonator")
    plt.xlabel("Power (dBm)")
    plt.ylabel("Reflected Voltage (mV)")

    plt.legend()
    plt.tick_params(axis='both', direction='in', top='true', right='true')
    plt.show()
