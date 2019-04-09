from utils import State


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

    scenario_quantities = (0, 1, 0, 0, 0, 0)
    scenario = State(0, *scenario_quantities)
    print(scenario)

    test_quantities = (0, 0, 0, 0, 0, 0)
    test = State(1, *test_quantities)

    test_quantities_2 = (0, 1, 0, 0, 0, 0)
    test_2 = State(2, *test_quantities_2)

    print(test == scenario)
    print(test_2 == scenario)


if __name__ == '__main__':
    main()
