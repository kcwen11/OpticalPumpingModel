import copy

# this file contains all the data about the spin states and their transitions for B = 145
# the ground state is 2S_1/2 and the excited state is 2P_1/2

energy_g = {'|2,-2)': -202 + 803, '|2,-1)': -53 + 803, '|2, 0)': 49 + 803, '|2, 1)': 132 + 803, '|2, 2)': 204 + 803,
            '|1,-1)': 52, '|1, 0)': -50, '|1, 1)': -132
            }  # in MHz, for ground states it is relative to the 2S_1/2, B = 0, F_g = 1 energy level
energy_e = {'e|2,-2)': -67, 'e|2,-1)': 14, 'e|2, 0)': 36, 'e|2, 1)': 53, 'e|2, 2)': 68,
            'e|1,-1)': -105, 'e|1, 0)': -127, 'e|1, 1)': -144
            }  # in MHz, for excited states it is relative to the 2P_1/2, B = 0, F_e = 2 energy level

# these are the allowed absorption transitions. most of the other dictionaries are structured based on this one.
# it is a nested dictionary (a dictionary with dictionaries inside it). it might be easier to think of it as a
# graph (like from graph theory, not like a plot). each state is a node, and each transition is an edge, with a
# direction and a value. each dictionary key on the left is a state an electron can be in,
# and the value for the state is another dictionary containing the possible transitions from the key it belongs to.
# in the secondary dictionary, the keys are states at the end of the transition, and the values are different
# characteristics of the transition, like frequency, rate, or relative strength
allowed_transitions = {'|2,-2)': {'e|2,-2)': 0, 'e|2,-1)': 0, 'e|1,-1)': 0},
                       '|2,-1)': {'e|2,-2)': 0, 'e|2,-1)': 0, 'e|2, 0)': 0, 'e|1,-1)': 0, 'e|1, 0)': 0},
                       '|2, 0)': {'e|2,-1)': 0, 'e|2, 0)': 0, 'e|2, 1)': 0, 'e|1,-1)': 0, 'e|1, 0)': 0, 'e|1, 1)': 0},
                       '|2, 1)': {'e|2, 0)': 0, 'e|2, 1)': 0, 'e|2, 2)': 0, 'e|1, 0)': 0, 'e|1, 1)': 0},
                       '|2, 2)': {'e|2, 1)': 0, 'e|2, 2)': 0, 'e|1, 1)': 0},
                       '|1,-1)': {'e|2,-2)': 0, 'e|2,-1)': 0, 'e|2, 0)': 0, 'e|1,-1)': 0, 'e|1, 0)': 0},
                       '|1, 0)': {'e|2,-1)': 0, 'e|2, 0)': 0, 'e|2, 1)': 0, 'e|1,-1)': 0, 'e|1, 0)': 0, 'e|1, 1)': 0},
                       '|1, 1)': {'e|2, 0)': 0, 'e|2, 1)': 0, 'e|2, 2)': 0, 'e|1, 0)': 0, 'e|1, 1)': 0}
                       }

# the relative strengths of the emission transitions
# see https://demonstrations.wolfram.com/TransitionStrengthsOfAlkaliMetalAtoms/
emit_str = {'e|2,-2)': {'|2,-2)': 1 / 3, '|2,-1)': 1 / 6, '|1,-1)': 1 / 2},
            'e|2,-1)': {'|2,-2)': 1 / 6, '|2,-1)': 1 / 12, '|2, 0)': 1 / 4, '|1,-1)': 1 / 4, '|1, 0)': 1 / 4},
            'e|2, 0)': {'|2,-1)': 1 / 4, '|2, 0)': 0, '|2, 1)': 1 / 4, '|1,-1)': 1 / 12, '|1, 0)': 1 / 3,
                        '|1, 1)': 1 / 12},
            'e|2, 1)': {'|2, 0)': 1 / 4, '|2, 1)': 1 / 12, '|2, 2)': 1 / 6, '|1, 0)': 1 / 4, '|1, 1)': 1 / 4},
            'e|2, 2)': {'|2, 1)': 1 / 6, '|2, 2)': 1 / 3, '|1, 1)': 1 / 2},
            'e|1,-1)': {'|2,-2)': 1 / 2, '|2,-1)': 1 / 4, '|2, 0)': 1 / 12, '|1,-1)': 1 / 12, '|1, 0)': 1 / 12},
            'e|1, 0)': {'|2,-1)': 1 / 4, '|2, 0)': 1 / 3, '|2, 1)': 1 / 4, '|1,-1)': 1 / 12, '|1, 0)': 0,
                        '|1, 1)': 1 / 12},
            'e|1, 1)': {'|2, 0)': 1 / 12, '|2, 1)': 1 / 4, '|2, 2)': 1 / 2, '|1, 0)': 1 / 12, '|1, 1)': 1 / 12}
            }  # this is the transition strength from each excited state to the ground states

# the relative strengths of the maximum cross section. this is emit_str flipped around
# (not exactly correct because pi polarized transitions have half the cross section of sigma polarized transitions,
# but I will take care of that later in the code)
abs_str = copy.deepcopy(allowed_transitions)  # deepcopy just makes a new dictionary with the same terms
for t, u in emit_str.items():
    for v, w in u.items():
        abs_str[v][t] = w

# I use this for loop a lot. for each state (t), I go through every possible transition listed in the (u) dictionary.
# for each state (v) in the corresponding (u) dictionary, there is an associated value (w), which can be the rate
# of the transition, its relative strength, or the frequency, depending on the situation. in this case, it is the
# relative strength
