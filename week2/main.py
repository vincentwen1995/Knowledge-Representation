import sys

# intialize the scenario.
scenario = dict()

scenario['quantities'] = dict()

scenario['quantities']['inflow'] = dict()
scenario['quantities']['inflow']['mag'] = '+'
scenario['quantities']['inflow']['space'] = ['0', '+']
scenario['quantities']['inflow']['de'] = '0'

scenario['quantities']['volume'] = dict()
scenario['quantities']['volume']['mag'] = '0'
scenario['quantities']['volume']['space'] = ['0', '+', 'max']
scenario['quantities']['volume']['de'] = '0'

scenario['quantities']['outflow'] = dict()
scenario['quantities']['outflow']['mag'] = '0'
scenario['quantities']['outflow']['space'] = ['0', '+', 'max']
scenario['quantities']['outflow']['de'] = '0'

scenario['influences'] = list()
scenario['influences'].append(['inflow', 'volume', 1])
scenario['influences'].append(['outflow', 'volume', -1])

scenario['proportionalities'] = list()
scenario['proportionalities'].append(['volume', 'outflow', 1])

scenario['constraints'] = list()
scenario['constraints'].append(['volume', 'outflow', 'max'])
scenario['constraints'].append(['volume', 'outflow', '0'])

print(scenario)
