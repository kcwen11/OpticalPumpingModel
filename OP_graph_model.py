import numpy as np
import beam_spectrum as spec
import beam_class
import state_data
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

A21 = beam_class.A21
gr = spec.rates  # this is the average rate of photon scattering for each transition when excited by our laser system

# see https://demonstrations.wolfram.com/TransitionStrengthsOfAlkaliMetalAtoms/
emit_str = state_data.emit_str

st = ['|2,-2)', '|2,-1)', '|2, 0)', '|2, 1)', '|2, 2)', '|1,-1)', '|1, 0)', '|1, 1)',
      'e|2,-2)', 'e|2,-1)', 'e|2, 0)', 'e|2, 1)', 'e|2, 2)', 'e|1,-1)', 'e|1, 0)', 'e|1, 1)']
# the order of the states in the variable [v] below follows the above variable [st]


# This is the differential equation
def state_rates(s, v):  # returns the derivative of each population in each state for given populations [v]
    dv = [0] * 16  # [dv] is the same size as [v]
    # for each transition from a ground state to an excited state, the rate per atom is stored in the dictionary {gr}
    for k, m in gr.items():
        for n, o in m.items():
            dv[st.index(k)] = dv[st.index(k)] - o * v[st.index(k)]
            dv[st.index(n)] = dv[st.index(n)] + o * v[st.index(k)]
    # for each transition from an excited state to a ground state, the rate per atom is a fraction of A21
    # the fraction is stored in the dictionary {emit_str} (stands for emission strength)
    for p, q in emit_str.items():
        for r, s in q.items():
            dv[st.index(p)] = dv[st.index(p)] - A21 * s * v[st.index(p)]
            dv[st.index(r)] = dv[st.index(r)] + A21 * s * v[st.index(p)]
    # the rate for a transition leaving a state is always proportional to the population in the state itself
    # the rate for a transition going into a state is proportional to the population of a different state
    return dv


# this solves the differential equation above for the initial condition: 100% of atoms in ground [2, -2)
OP_model_input = solve_ivp(state_rates, (0, 5 * 10 ** -5), [100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           t_eval=np.arange(0, 5 * 10 ** -5 + 10 ** -6, 10 ** -6))

for q in range(8):
    plt.plot(OP_model_input.t, OP_model_input.y.T[:, q:q + 1], label=st[q])
plt.title('Percent of atoms in each ground state vs time')
plt.xlabel('Time (s)')
plt.ylabel('Percent')
plt.legend()
plt.show()

for q in range(8, 16):
    plt.plot(OP_model_input.t, OP_model_input.y.T[:, q:q + 1], label=st[q])
plt.title('Percent of atoms in each excited state vs time')
plt.xlabel('Time (s)')
plt.ylabel('Percent')
plt.legend()
plt.show()

total = OP_model_input.y.T[:, 15:16]
for i in range(15):
    total = total + OP_model_input.y.T[:, i:i + 1]

plt.plot(OP_model_input.t, total, label='total')
plt.title('Total percent of atoms vs time')
plt.xlabel('Time (s)')
plt.ylabel('Percent')
plt.show()

# this solves the differential equation above for the initial condition: 100% of atoms in ground [2, 2)
OP_model_ring = solve_ivp(state_rates, (0, 5 * 10 ** -5), [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          t_eval=np.arange(0, 5 * 10 ** -5 + 10 ** -6, 10 ** -6))

plt.plot(OP_model_ring.t, OP_model_ring.y.T)
plt.title('After a cycle in the ring, percent of atoms in each ground state vs time')
plt.xlabel('Time (s)')
plt.ylabel('Percent')
plt.show()

print('#########################################################################################')
print('percent in |2, 2) after initial input: ', OP_model_input.y.T[:, 4:5][-1])
print('percent in |2, 2) after a cycle in the ring: ', OP_model_ring.y.T[:, 4:5][-1])
print('percent in |2, 1) and |2, 2) after a cycle in the ring: ', OP_model_ring.y.T[:, 3:4][-1] +
      OP_model_ring.y.T[:, 4:5][-1])
print('number of cycles until half atoms lost: ', np.log(1 / 2) / np.log(OP_model_ring.y.T[:, 4:5][-1] / 100))
