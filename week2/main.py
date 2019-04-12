from utils import *
from itertools import product
import copy


def main():
    print('-----------------------------')
    print('Assumptions:')
    print('- Inflow behavior: positive parabola')
    print('- Inflow intitial magnitude: 0')
    print('- Inflow intitial derivative: +')
    print('- Volume intitial magnitude: 0')
    print('- Volume intitial derivative: 0')
    print('- Outflow intitial magnitude: 0')
    print('- Outflow intitial derivative: 0')
    print('-----------------------------')
    print('Applying Qualitative Reasoning...')
    scenario_quantities = (0, 1, 0, 0, 0, 0)
    scenario = State(1, 0, *scenario_quantities)
    solver = Flow(scenario)
    result = solver.search()
    plotter = Visualizer(result)
    plotter.draw_states()
    plotter.output_graph()
    plotter.output_trace()
    print('-----------------------------')
    print('Done!')
    print('-----------------------------')
    print('The total number of states: {}'.format(len(result)))
    print('-----------------------------')
    print('The state graph is exported to ./result/state_graph.pdf')
    print('The trace file is exported to ./result/trace.txt')
    print('-----------------------------')


if __name__ == '__main__':
    main()
