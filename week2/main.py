from utils import State, Flow


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
    print(test)

    inflow_mags = State.propagate_inflow_mag(test)
    vol_ders = State.propagate_vol_der(test)
    vol_mags = State.propagate_vol_mag(test)
    outflow_ders = State.propagate_vol_der(test)
    outflow_mags = State.propagate_vol_mag(test)

    print(inflow_mags)
    print(vol_ders)
    print(vol_mags)
    print(outflow_ders)
    print(outflow_mags)


if __name__ == '__main__':
    main()
