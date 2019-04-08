import sys

# intialize the scenario.
quantity = dict()
quantity['Inflow'] = dict()
quantity['Inflow']['mag'] = '0'
quantity['Inflow']['values'] = ['0', '+']
quantity['Inflow']['de'] = '0'

quantity['Volume'] = dict()
quantity['Volume']['mag'] = '0'
quantity['Inflow']['values'] = ['0', '+', 'max']
quantity['Volume']['de'] = '0'

quantity['Outflow'] = dict()
quantity['Outflow']['mag'] = '0'
quantity['Inflow']['values'] = ['0', '+', 'max']
quantity['Outflow']['de'] = '0'

print(quantity)
