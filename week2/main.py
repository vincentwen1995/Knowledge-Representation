from utils import State, Flow
from itertools import product
import copy


def main():
    # # intialize the scenario.
    # scenario = dict()

    # scenario['quantities'] = dict()

    # scenario['quantities']['inflow'] = dict()
    # scenario['quantities']['inflow']['mag'] = '+'
    # scenario['quantities']['inflow']['space'] = ['0', '+']
    # scenario['quantities']['inflow']['de'] = '0'

    # scenario['quantities']['volume'] = dict()
    # scenario['quantities']['volume']['mag'] = '0'
    # scenario['quantities']['volume']['space'] = ['0', '+', 'max']
    # scenario['quantities']['volume']['de'] = '0'

    # scenario['quantities']['outflow'] = dict()
    # scenario['quantities']['outflow']['mag'] = '0'
    # scenario['quantities']['outflow']['space'] = ['0', '+', 'max']
    # scenario['quantities']['outflow']['de'] = '0'

    # scenario['influences'] = list()
    # scenario['influences'].append(['inflow', 'volume', 1])
    # scenario['influences'].append(['outflow', 'volume', -1])

    # scenario['proportionalities'] = list()
    # scenario['proportionalities'].append(['volume', 'outflow', 1])

    # scenario['constraints'] = list()
    # scenario['constraints'].append(['volume', 'outflow', 'max'])
    # scenario['constraints'].append(['volume', 'outflow', '0'])

    # print(scenario)

    # scenario_quantities = (0, 1, 0, 0, 0, 0)
    # scenario = State(0, -1, *scenario_quantities)
    # print(scenario)

    test_quantities = (1, 1, 1, 1, 1, 1)
    test = State(3, 2, *test_quantities)
    # test_quantities = (1, 1, 1, 0, 2, 0)
    # test = State(9, 3, *test_quantities)
    print(test)

    # inflow_mags = State.propagate_inflow_mag(test)
    # vol_ders = State.propagate_vol_der(test)
    # vol_mags = State.propagate_vol_mag(test)
    # outflow_ders = State.propagate_vol_der(test)
    # outflow_mags = State.propagate_outflow_mag(test)

    # print('Inflow Magnitudes: ')
    # print(inflow_mags)
    # print('Volume Derivatives: ')
    # print(vol_ders)
    # print('Volume Magnitudes: ')
    # print(vol_mags)
    # print('Outflow Derivatives')
    # print(outflow_ders)
    # print('Outflow Magnitudes: ')
    # print(outflow_mags)

    # states_from_state3 = list(product(inflow_mags, [1, 0], vol_mags, vol_ders, outflow_mags, outflow_ders))
    states_from_state3 = list(product(State.inflow_qs, State.der_qs, State.vol_qs, State.der_qs, State.outflow_qs, State.der_qs))
    for potential_perm in copy.deepcopy(states_from_state3):
        if potential_perm == test.get_tuple():
            states_from_state3.remove(potential_perm)
            continue
        # print('potential_perm: \n')
        # print(potential_perm)
        potential_state = State(0, 3, *potential_perm)
        if State.check_influence(test, potential_state) and \
                State.check_max_clipping(potential_state) and \
                State.check_min_clipping(potential_state) and \
                State.check_value_constraint(potential_state) and \
                State.check_proportionality(potential_state) and \
                State.check_continuity(test, potential_state) and \
                State.check_exogenous_inflow(test, potential_state):
            continue
        else:
            states_from_state3.remove(potential_perm)

    print('All possible combinations: ')
    print(states_from_state3)
    print(len(states_from_state3))


if __name__ == '__main__':
    main()
