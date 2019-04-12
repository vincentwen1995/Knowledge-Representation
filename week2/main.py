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
    print('The total number of all states: {}'.format(len(result)))


if __name__ == '__main__':
    main()
