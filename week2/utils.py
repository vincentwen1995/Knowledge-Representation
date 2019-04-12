import copy
import pydot
import os
from itertools import product


class State:
    der_qs = (-1, 0, 1)
    inflow_qs = (0, 1)
    outflow_qs = (0, 1, 2)
    vol_qs = (0, 1, 2)
    str_mag_qs = {0: '0', 1: '+', 2: 'max'}
    str_der_qs = {-1: '-', 0: '0', 1: '+'}

    def __init__(self, id, parent_id, inflow_mag, inflow_der, vol_mag, vol_der, outflow_mag, outflow_der):
        self.id = id
        self.parent_ids = [parent_id]
        self.inflow_mag = inflow_mag
        self.inflow_der = inflow_der
        self.outflow_mag = outflow_mag
        self.outflow_der = outflow_der
        self.vol_mag = vol_mag
        self.vol_der = vol_der

    def __str__(self):
        return 'State id: {}\n'.format(self.id) \
            + 'Parent ids: {}\n'.format(self.parent_ids) \
            + 'Inflow Magnitude: {}\n'.format(State.str_mag_qs[self.inflow_mag]) \
            + 'Inflow Derivative: {}\n'.format(State.str_der_qs[self.inflow_der]) \
            + 'Volume Magnitude: {}\n'.format(State.str_mag_qs[self.vol_mag]) \
            + 'Volume Derivative: {}\n'.format(State.str_der_qs[self.vol_der]) \
            + 'Outflow Magnitude: {}\n'.format(State.str_mag_qs[self.outflow_mag]) \
            + 'Outflow Derivative: {}\n'.format(State.str_der_qs[self.outflow_der])

    def __eq__(self, other):
        return self.inflow_mag == other.inflow_mag and \
            self.inflow_der == other.inflow_der and \
            self.vol_mag == other.vol_mag and \
            self.vol_der == other.vol_der and \
            self.outflow_mag == other.outflow_mag and \
            self.outflow_der == other.outflow_der

    def diff(self, other):
        '''Serialize the difference in the transition from other(parent) to self(child).

        Args:
            other ([State]): the parent state of self

        Returns:
            [str]: serialized changes
        '''

        result = ''
        if self.inflow_mag != other.inflow_mag:
            result += 'In  Mag:  {:^3}  -->  {:^3}\n'.format(State.str_mag_qs[other.inflow_mag], State.str_mag_qs[self.inflow_mag])
        if self.inflow_der != other.inflow_der:
            result += 'In  Der:  {:^3}  -->  {:^3}\n'.format(State.str_der_qs[other.inflow_der], State.str_der_qs[self.inflow_der])

        if self.vol_mag != other.vol_mag:
            result += 'Vol Mag:  {:^3}  -->  {:^3}\n'.format(State.str_mag_qs[other.vol_mag], State.str_mag_qs[self.vol_mag])
        if self.vol_der != other.vol_der:
            result += 'Vol Der:  {:^3}  -->  {:^3}\n'.format(State.str_der_qs[other.vol_der], State.str_der_qs[self.vol_der])

        if self.outflow_mag != other.outflow_mag:
            result += 'Out Mag:  {:^3}  -->  {:^3}\n'.format(State.str_mag_qs[other.outflow_mag], State.str_mag_qs[self.outflow_mag])
        if self.outflow_der != other.outflow_der:
            result += 'Out Der:  {:^3}  -->  {:^3}\n'.format(State.str_der_qs[other.outflow_der], State.str_der_qs[self.outflow_der])

        return result

    def get_tuple(self):
        '''Get the quantity values in a tuple.

        Returns:
            [tuple]: tuple of quantity values
        '''

        return (self.inflow_mag, self.inflow_der, self.vol_mag, self.vol_der, self.outflow_mag, self.outflow_der)

    @staticmethod
    def check_influence(state, potential_state):
        '''Check whether the influence relations I+(inflow, volume) and I-(outflow, volume) are satisfied.

        Args:
            state ([State]): starting state
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        if state.inflow_mag >= state.outflow_mag and \
                state.inflow_mag <= potential_state.inflow_mag and \
                state.outflow_mag >= potential_state.outflow_mag and \
                potential_state.inflow_der >= potential_state.outflow_der:
            if potential_state.vol_der <= state.vol_der:
                if not ((potential_state.inflow_der == State.der_qs[1] and
                         potential_state.outflow_der == State.der_qs[1]) or
                        (potential_state.inflow_der == State.der_qs[0] and
                         potential_state.outflow_der == State.der_qs[0])):
                    return False

        if potential_state.inflow_mag == State.inflow_qs[0] and \
                potential_state.outflow_mag > potential_state.inflow_mag:
            if not potential_state.vol_der == State.der_qs[0]:
                return False

        if potential_state.outflow_mag == State.outflow_qs[0] and \
                potential_state.inflow_mag > potential_state.outflow_mag:
            if not potential_state.vol_der == State.der_qs[2]:
                return False

        if state.vol_der == State.der_qs[1]:
            if potential_state.inflow_der >= state.inflow_der and \
                    potential_state.outflow_der <= state.outflow_der:
                if potential_state.vol_der < State.der_qs[1] and \
                        not (potential_state.inflow_mag < potential_state.outflow_mag and
                             (potential_state.outflow_mag != state.outflow_mag or
                              potential_state.inflow_mag == State.inflow_qs[0])):
                    return False
            if potential_state.inflow_der <= state.inflow_der and \
                    potential_state.outflow_der >= state.outflow_der:
                if potential_state.vol_der > State.der_qs[1] and \
                        not (potential_state.inflow_mag > potential_state.outflow_mag and
                             potential_state.inflow_mag != state.inflow_mag):
                    return False
            if potential_state.inflow_mag == State.inflow_qs[0] and \
                    potential_state.outflow_mag != State.outflow_qs[0]:
                if not potential_state.vol_der == State.der_qs[0]:
                    return False
        return True

    @staticmethod
    def check_max_clipping(potential_state):
        '''Check whether the derivative is clipped to 0 when the magnitude reaches maximum.

        Args:
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        # When the volume magnitude is max, the derivative should not be +.
        if potential_state.vol_mag == State.vol_qs[2] and potential_state.vol_der == State.der_qs[2]:
            return False
        # When the outflow magnitude is max, the derivative should not be +.
        if potential_state.outflow_mag == State.outflow_qs[2] and potential_state.outflow_der == State.der_qs[2]:
            return False
        return True

    @staticmethod
    def check_min_clipping(potential_state):
        '''Check whether the derivative is clipped to 0 when the magnitude reaches 0.

        Args:
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        # When the inflow magnitude is 0, the derivative should not be -.
        if potential_state.inflow_mag == State.inflow_qs[0] and potential_state.inflow_der == State.der_qs[0]:
            return False
        # When the volume magnitude is 0, the derivative should not be -.
        if potential_state.vol_mag == State.vol_qs[0] and potential_state.vol_der == State.der_qs[0]:
            return False
        # When the outflow magnitude is 0, the derivative should not be -.
        if potential_state.outflow_mag == State.outflow_qs[0] and potential_state.outflow_der == State.der_qs[0]:
            return False
        return True

    @staticmethod
    def check_proportionality(potential_state):
        '''Check whether the proportionality relation P+(volume, outflow) is satisfied.

        Args:
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        if potential_state.outflow_der != potential_state.vol_der:
            return False
        return True

    @staticmethod
    def check_continuity(state, potential_state):
        '''Check whether the continuity constraint for all the quantities are satisfied.

        Args:
            state ([State]): starting state
            potential_state ([State]): ending state

        Returns:
            [boolean]: [description]
        '''

        if abs(potential_state.inflow_mag - state.inflow_mag) > 1:
            return False
        if abs(potential_state.inflow_der - state.inflow_der) > 1:
            return False
        if abs(potential_state.vol_mag - state.vol_mag) > 1:
            return False
        if abs(potential_state.vol_der - state.vol_der) > 1:
            return False
        if abs(potential_state.outflow_mag - state.outflow_mag) > 1:
            return False
        if abs(potential_state.outflow_der - state.outflow_der) > 1:
            return False
        return True

    @staticmethod
    def check_exogenous_inflow(state, potential_state):
        '''Check whether the sequence of exogenous inflow derivatives is satisfied.

        Args:
            state ([State]): starting state
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        if state.inflow_der == State.der_qs[1] and potential_state.inflow_der == State.der_qs[2]:
            return False
        if potential_state.inflow_der == State.der_qs[1] and state.inflow_der == State.der_qs[0]:
            if potential_state.inflow_mag == State.inflow_qs[1]:
                return False
        return True

    @staticmethod
    def check_value_constraint(potential_state):
        '''Check whether the value constraints between volume and outflow are satisfied.

        Args:
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        if (potential_state.vol_mag == State.vol_qs[0] or potential_state.vol_mag == State.vol_qs[2]) and potential_state.outflow_mag != potential_state.vol_mag:
            return False
        else:
            return True

    @staticmethod
    def check_simultaneous_change(state, potential_state):
        '''Check whether there are simultaneous changes in the magnitudes and derivatives.

        Args:
            state ([State]): starting state
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        if potential_state.inflow_mag != state.inflow_mag and \
                potential_state.inflow_der != state.inflow_der:
            if not potential_state.inflow_mag == State.inflow_qs[0]:
                return False
        if potential_state.vol_mag != state.vol_mag and \
                potential_state.vol_der != state.vol_der:
            if not (potential_state.vol_mag == State.vol_qs[0] or
                    potential_state.vol_mag == State.vol_qs[2]):
                return False

        if potential_state.outflow_mag != state.outflow_mag and \
                potential_state.outflow_der != state.outflow_der:
            if not (potential_state.outflow_mag == State.outflow_qs[0] or
                    potential_state.outflow_mag == State.outflow_qs[2]):
                return False
        if (potential_state.outflow_mag == State.outflow_qs[1] and
            state.outflow_mag == State.outflow_qs[0]) or \
            (potential_state.vol_mag == State.vol_qs[1] and
             state.vol_mag == State.vol_qs[0]):
            if potential_state.inflow_der != state.inflow_der:
                return False
        return True

    @staticmethod
    def check_point_values(state, potential_state):
        '''Check whether immediate transitions from point values are satisfied and the directions of transitions are correct.

        Args:
            state ([State]): starting state
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        if state.inflow_mag == State.inflow_qs[0]:
            if state.inflow_der == State.der_qs[0] and \
                    potential_state.inflow_mag >= state.inflow_mag:
                return False
            elif state.inflow_der == State.der_qs[1] and \
                    potential_state.inflow_mag != state.inflow_mag:
                return False
            elif state.inflow_der == State.der_qs[2] and \
                    potential_state.inflow_mag <= state.inflow_mag:
                return False

        if state.vol_mag == State.vol_qs[0] or state.vol_mag == State.vol_qs[2]:
            if state.vol_der == State.der_qs[0] and \
                    potential_state.vol_mag >= state.vol_mag:
                return False
            elif state.vol_der == State.der_qs[1] and \
                    potential_state.vol_mag != state.vol_mag:
                return False
            elif state.vol_der == State.der_qs[2] and \
                    potential_state.vol_mag <= state.vol_mag:
                return False

        if state.outflow_mag == State.outflow_qs[0] or state.outflow_mag == State.outflow_qs[2]:
            if state.outflow_der == State.der_qs[0] and \
                    potential_state.outflow_mag >= state.outflow_mag:
                return False
            elif state.outflow_der == State.der_qs[1] and \
                    potential_state.outflow_mag != state.outflow_mag:
                return False
            elif state.outflow_der == State.der_qs[2] and \
                    potential_state.outflow_mag <= state.outflow_mag:
                return False

        return True

    @staticmethod
    def check_impossible_states(potential_state):
        '''Filter out impossible states.

        Args:
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        if potential_state.inflow_mag == State.inflow_qs[1] and potential_state.inflow_der == State.der_qs[0] and \
            potential_state.vol_mag == State.vol_qs[0] and potential_state.vol_der == State.der_qs[1] and \
                potential_state.outflow_mag == State.outflow_qs[0] and potential_state.outflow_der == State.der_qs[1]:
            return False
        return True

    @staticmethod
    def check_interval_values(state, potential_state):
        '''Check whether interval transitions from interval values are satisfied and the directions of transitions are correct.

        Args:
            state ([State]): starting state
            potential_state ([State]): ending state

        Returns:
            [boolean]: 
        '''

        if state.inflow_mag == State.inflow_qs[1]:
            if state.inflow_der == State.der_qs[0] and \
                    potential_state.inflow_mag > state.inflow_mag:
                return False
            elif state.inflow_der == State.der_qs[1] and \
                    potential_state.inflow_mag != state.inflow_mag:
                return False
            elif state.inflow_der == State.der_qs[2] and \
                    potential_state.inflow_mag < state.inflow_mag:
                return False

        if state.vol_mag == State.vol_qs[1]:
            if state.vol_der == State.der_qs[0] and \
                    potential_state.vol_mag > state.vol_mag:
                return False
            elif state.vol_der == State.der_qs[1] and \
                    potential_state.vol_mag != state.vol_mag:
                return False
            elif state.vol_der == State.der_qs[2] and \
                    potential_state.vol_mag < state.vol_mag:
                return False

        if state.outflow_mag == State.outflow_qs[1]:
            if state.outflow_der == State.der_qs[0] and \
                    potential_state.outflow_mag > state.outflow_mag:
                return False
            elif state.outflow_der == State.der_qs[1] and \
                    potential_state.outflow_mag != state.outflow_mag:
                return False
            elif state.outflow_der == State.der_qs[2] and \
                    potential_state.outflow_mag < state.outflow_mag:
                return False
        return True


class Flow:

    def __init__(self, scenario):
        self.scenario = scenario

    def search(self):
        '''Conduct breadth-first search from the initial state.

        Returns:
            [list]: list of states
        '''

        # Initialize variables.
        states = [self.scenario]
        visited_states = []
        parent_state = self.scenario
        counter = 2

        # Terminate when there is no more parent_state set up.
        while parent_state:
            # Generate all the permutations of the state space.
            state_space_perms = list(product(State.inflow_qs, State.der_qs, State.vol_qs, State.der_qs, State.outflow_qs, State.der_qs))
            # Search through the permutations and remove the implausible ones.
            for potential_perm in copy.deepcopy(state_space_perms):
                if potential_perm == parent_state.get_tuple():
                    state_space_perms.remove(potential_perm)
                    continue

                potential_state = State(-1, -1, *potential_perm)
                if State.check_influence(parent_state, potential_state) and \
                        State.check_max_clipping(potential_state) and \
                        State.check_min_clipping(potential_state) and \
                        State.check_value_constraint(potential_state) and \
                        State.check_proportionality(potential_state) and \
                        State.check_continuity(parent_state, potential_state) and \
                        State.check_exogenous_inflow(parent_state, potential_state) and \
                        State.check_simultaneous_change(parent_state, potential_state) and \
                        State.check_point_values(parent_state, potential_state) and \
                        State.check_interval_values(parent_state, potential_state) and \
                        State.check_impossible_states(potential_state):
                    continue
                else:
                    state_space_perms.remove(potential_perm)
            # For every plausible child state,
            # if it already exists, record the current parent state's id;
            # if it does not exist, add it to the states queue.
            for child_state_perm in state_space_perms:
                tmp = State(counter, parent_state.id, *child_state_perm)
                exist = False
                for state in states:
                    if state == tmp:
                        state.parent_ids.append(parent_state.id)
                        exist = True
                        break
                if not exist:
                    states.append(tmp)
                    counter += 1
            # Add the parent_state to the visited list.
            visited_states.append(parent_state)
            parent_state = None
            # Find the first non-visited state in the states queue and set it as the next parent state.
            for state in states:
                if state not in visited_states:
                    parent_state = state
                    break
        return states


class Visualizer:

    def __init__(self, states):
        self.states_dict = {state.id: state for state in states}
        self.states = states
        self.graph = pydot.Dot(graph_type='digraph')

    def draw_states(self):
        '''Given the list of states, generate the graph with nodes and edges.
        '''

        # For every state, generate a node in the graph with intra-state information.
        nodes = dict()
        for state in self.states:
            state_node = pydot.Node('State {}\nInflow({}, {})\nVolume({}, {})\nOutflow({}, {})'
                                    .format(state.id, State.str_mag_qs[state.inflow_mag], State.str_der_qs[state.inflow_der], State.str_mag_qs[state.vol_mag], State.str_der_qs[state.vol_der], State.str_mag_qs[state.outflow_mag], State.str_der_qs[state.outflow_der]),
                                    shape='box')
            nodes[state.id] = state_node
            self.graph.add_node(state_node)
        # For every state, connnect the edges between itself and its children.
        for state in self.states:
            if state.id != 1:
                for parent_id in state.parent_ids:
                    # self.graph.add_edge(pydot.Edge(nodes[parent_id], nodes[state.id], label=state.diff(self.states_dict[parent_id])))
                    self.graph.add_edge(pydot.Edge(nodes[parent_id], nodes[state.id]))

    def output_graph(self):
        '''Output the generated graph to pdf file.
        '''

        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, 'result')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.graph.write_pdf(os.path.join(dirname, 'state_graph.pdf'))

    def output_trace(self):
        '''Output the inter-state transition information into a trace file.
        '''

        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, 'result')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(os.path.join(dirname, 'trace.txt'), 'w') as trace_file:
            for state in self.states:
                for child_state in self.states:
                    if state.id in child_state.parent_ids:
                        trace_file.write('State {:<2}  -->  State {:<2}:    '.format(state.id, child_state.id) +
                                         state.diff(child_state).replace('\n', '    ') + '\n')
