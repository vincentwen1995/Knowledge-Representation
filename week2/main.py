from utils import *
from itertools import product
import copy


def main():

    scenario_quantities = (0, 1, 0, 0, 0, 0)
    scenario = State(1, 0, *scenario_quantities)
    solver = Flow(scenario)
    result = solver.search()
    plotter = Visualizer(result)
    plotter.draw_states()
    plotter.output_graph()
    plotter.output_trace()
    print('The total number of all states:', len(result))

    # test_quantities = (0, 1, 0, 0, 0, 0)
    # test = State(1, 0, *test_quantities)
    # test_quantities = (1, 1, 0, 1, 0, 1)
    # test = State(2, 1, *test_quantities)
    # test_quantities = (1, 1, 1, 1, 1, 1)
    # test = State(3, 2, *test_quantities)
    # test_quantities = (1, 0, 2, 0, 2, 0)
    # test = State(4, 3, *test_quantities)
    # test_quantities = (1, 0, 1, 0, 2, 0)
    # test = State(5, 3, *test_quantities)
    # test_quantities = (1, 1, 2, 0, 2, 0)
    # test = State(6, 3, *test_quantities)
    # test_quantities = (1, 0, 1, 0, 1, 0)
    # test = State(7, 3, *test_quantities)
    # test_quantities = (1, 0, 1, 1, 1, 1)
    # test = State(8, 3, *test_quantities)
    # test_quantities = (1, 1, 1, 0, 2, 0)
    # test = State(9, 3, *test_quantities)
    # test_quantities = (1, 0, 1, -1, 2, -1)
    # test = State(10, 9, *test_quantities)
    # test_quantities = (1, -1, 2, 0, 2, 0)
    # test = State(11, 4, *test_quantities)
    # test_quantities = (1, -1, 1, 0, 2, 0)
    # test = State(12, 5, *test_quantities)
    # test_quantities = (1, -1, 1, 1, 1, 1)
    # test = State(13, 7, *test_quantities)
    # test_quantities = (1, -1, 1, -1, 1, -1)
    # test = State(14, 10, *test_quantities)
    # test_quantities = (1, -1, 1, 0, 1, 0)
    # test = State(15, 7, *test_quantities)
    # test_quantities = (1, 0, 2, -1, 2, -1)
    # test = State(16, 6, *test_quantities)
    # test_quantities = (1, -1, 1, -1, 2, -1)
    # test = State(17, 5, *test_quantities)
    # test_quantities = (1, -1, 2, -1, 2, -1)
    # test = State(18, 4, *test_quantities)
    # test_quantities = (1, 0, 1, -1, 1, -1)
    # test = State(19, 10, *test_quantities)
    # test_quantities = (0, 0, 1, -1, 1, -1)
    # test = State(20, 14, *test_quantities)
    # test_quantities = (0, 0, 0, 0, 0, 0)
    # test = State(21, 14, *test_quantities)
    # test_quantities = (0, 0, 1, 0, 0, 0)
    # test = State(22, 14, *test_quantities)
    # test_quantities = (0, 0, 1, -1, 2, -1)
    # test = State(23, 12, *test_quantities)
    test_quantities = (0, 0, 2, -1, 2, -1)
    test = State(24, 11, *test_quantities)
    print('\nTest state:')
    print(test)

    test_state = list(product(State.inflow_qs, State.der_qs, State.vol_qs, State.der_qs, State.outflow_qs, State.der_qs))
    for potential_perm in copy.deepcopy(test_state):
        if potential_perm == test.get_tuple():
            test_state.remove(potential_perm)
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
                State.check_exogenous_inflow(test, potential_state) and \
                State.check_simultaneous_change(test, potential_state) and \
                State.check_point_values(test, potential_state) and \
                State.check_interval_values(test, potential_state):
            continue
        else:
            test_state.remove(potential_perm)

    print('All possible combinations: ')
    print(test_state)
    print('\nThe number of states generated from the test state:', len(test_state))


if __name__ == '__main__':
    main()
