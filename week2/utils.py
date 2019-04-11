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
        result = ''
        if self.inflow_mag != other.inflow_mag:
            result += 'In Mag: {} -> {}\n'.format(State.str_mag_qs[other.inflow_mag], State.str_mag_qs[self.inflow_mag])
        if self.inflow_der != other.inflow_der:
            result += 'In Der: {} -> {}\n'.format(State.str_der_qs[other.inflow_der], State.str_der_qs[self.inflow_der])

        if self.vol_mag != other.vol_mag:
            result += 'Vol Mag: {} -> {}\n'.format(State.str_mag_qs[other.vol_mag], State.str_mag_qs[self.vol_mag])
        if self.vol_der != other.vol_der:
            result += 'Vol Der: {} -> {}\n'.format(State.str_der_qs[other.vol_der], State.str_der_qs[self.vol_der])

        if self.outflow_mag != other.outflow_mag:
            result += 'Out Mag: {} -> {}\n'.format(State.str_mag_qs[other.outflow_mag], State.str_mag_qs[self.outflow_mag])
        if self.outflow_der != other.outflow_der:
            result += 'Out Der: {} -> {}\n'.format(State.str_der_qs[other.outflow_der], State.str_der_qs[self.outflow_der])

        return result

    def get_tuple(self):
        return (self.inflow_mag, self.inflow_der, self.vol_mag, self.vol_der, self.outflow_mag, self.outflow_der)

    @staticmethod
    def propagate_inflow_mag(state):
        '''Use the exogenous inflow derivative
        to propagate the magnitude of the inflow.

        Returns:
            [int]: possible values for the inflow magnitude
        '''

        inflow_mags = []
        # With zero inflow derivative in the start state,
        # the magnitude remains the same.
        if state.inflow_der == State.der_qs[1]:
            inflow_mags.append(state.inflow_mag)
        # With + inflow derivative in the start state,
        # the magnitude becomes + (immediate transition from 0 if + derivative).
        elif state.inflow_der == State.der_qs[2]:
            inflow_mags.append(State.inflow_qs[1])
        # With - inflow derivative in the start state,
        # the magnitude is either + or 0 (interval transition from +).
        else:
            inflow_mags.extend(State.inflow_qs[0:State.inflow_qs.index(state.inflow_mag) + 1])

        return inflow_mags

    @staticmethod
    def propagate_vol_der(state):
        '''Use the influence I+(inflow, volume) and influence I-(outflow, volume) 
        to propagate the derivative of the volume.

        Returns:
            [int]: possible values for the volume derivative
        '''

        vol_ders = []
        # With 0 outflow magnitude,
        # the volume derivative depends on the inflow magnitude (I+).
        if state.outflow_mag == State.outflow_qs[0]:
            # If the inflow magnitude is +,
            # the volume derivative becomes +.
            if state.inflow_mag == State.inflow_qs[1]:
                vol_ders.append(State.der_qs[2])
            # If the inflow magnitude is 0,
            # the volume derivative remains the same.
            else:
                vol_ders.append(state.vol_der)
        # With + or max outflow magnitude,
        # the volume derivative depends on
        # both the inflow and the outflow magnitudes (I+ and I-).
        else:
            # If the inflow magnitude is 0,
            # the volume derivative becomes -.
            if state.inflow_mag == State.inflow_qs[0]:
                vol_ders.append(State.der_qs[0])
            # If the inflow magnitude is +,
            # the volume derivative is ambiguous.
            else:
                vol_ders.extend(State.der_qs)

        # Apply continuity constraint s.t. there is no jump in the derivative.
        tmp = copy.deepcopy(vol_ders)
        for vol_der in tmp:
            if abs(vol_der - state.vol_der) > 1:
                vol_ders.remove(vol_der)

        return vol_ders

    @staticmethod
    def propagate_vol_mag(state):
        '''Use the volume derivative to propagate the volume magnitude.

        Returns:
            [int]: possible values for the volume magnitude
        '''

        vol_mags = []
        # With zero volume derivative,
        # the volume maginitude remains the same.
        if state.vol_der == State.der_qs[1]:
            vol_mags.append(state.vol_mag)
        # With + volume derivative,
        # the volume magnitude depends on its previous value.
        elif state.vol_der == State.der_qs[2]:
            # If the previous value is 0,
            # it becomes + (immediate transition).
            if state.vol_mag == State.vol_qs[0]:
                vol_mags.append(State.vol_qs[1])
            # If the previous value is +,
            # it can be either + or max (interval transition).
            elif state.vol_mag == State.vol_qs[1]:
                vol_mags.extend(State.vol_qs[1:3])
            # If the previous value is max,
            # it remains max.
            else:
                vol_mags.append(state.vol_mag)
        # With - volume derivative,
        # the volume magnitude depends on its previous value.
        else:
            # If the previous value is 0,
            # it remains 0.
            if state.vol_mag == State.vol_qs[0]:
                vol_mags.append(state.vol_mag)
            # If the previous value is +,
            # it can be either 0 or + (interval transition).
            elif state.vol_mag == State.vol_qs[1]:
                vol_mags.extend(State.vol_qs[0:2])
            # If the previous value is max,
            # it becomes + (immediate transition).
            else:
                vol_mags.append(State.vol_qs[1])

        # Apply continuity constraint s.t. there is no jump in the magnitude.
        tmp = copy.deepcopy(vol_mags)
        for vol_mag in tmp:
            if abs(vol_mag - state.vol_mag) > 1:
                vol_mags.remove(vol_mag)

        return vol_mags

    @staticmethod
    def propagate_outflow_der(state):
        '''Use the proportionality P+(volume, outflow)
        to propagate the derivative of the outflow.

        Returns:
            [int]: possible values for the outflow derivative
        '''

        outflow_ders = []
        outflow_ders.append(state.vol_der)
        return outflow_ders

    @staticmethod
    def propagate_outflow_mag(state):
        outflow_mags = []
        # With 0 volume magnitude,
        # the outflow magnitude becomes 0 (V).
        if state.vol_mag == State.vol_qs[0]:
            outflow_mags.append(State.outflow_qs[0])
        # With max volume maginitude,
        # the outflow magnitude becomes max (V).
        elif state.vol_mag == State.vol_qs[2]:
            outflow_mags.append(State.outflow_qs[2])
        # With + volume magnitude,
        # the outflow magnitude depends on the outflow derivative (no value contrains).
        else:
            # If the outflow derivative is 0,
            # the outflow magnitude remains the same.
            if state.outflow_der == State.der_qs[1]:
                outflow_mags.append(state.outflow_mag)
            # If the outflow derivative is +,
            # the outflow magnitude depends on its previous value.
            elif state.outflow_der == State.der_qs[2]:
                # If the previous value of outflow magnitude is 0,
                # it becomes + (immediate transition).
                if state.outflow_mag == State.outflow_qs[0]:
                    outflow_mags.append(State.outflow_qs[1])
                # If the previous value of outflow magnitude is +,
                # it can be either + or max (interval transition).
                elif state.outflow_mag == State.outflow_qs[1]:
                    outflow_mags.extend(State.outflow_qs[1:3])
                # If the previous value of outflow magnitude is max,
                # it remains the same.
                else:
                    outflow_mags.append(state.outflow_mag)
            # If the outflow derivative is -,
            # the outflow magnitude depends on its previous value.
            else:
                # If the previous value of outflow magnitude is 0,
                # it remains 0.
                if state.outflow_mag == State.outflow_qs[0]:
                    outflow_mags.append(state.outflow_mag)
                # If the previous value of outflow magnitude is +,
                # it can be either + or 0 (interval transition).
                elif state.outflow_mag == State.outflow_qs[1]:
                    outflow_mags.extend(State.outflow_qs[0:2])
                # If the previous value of outflow magnitude is max,
                # it becomes + (immediate transition).
                else:
                    outflow_mags.append(State.outflow_qs[1])
        return outflow_mags

    @staticmethod
    def check_influence(state, potential_state):

        if state.inflow_mag >= state.outflow_mag and \
                state.inflow_mag <= potential_state.inflow_mag and \
                state.outflow_mag >= potential_state.outflow_mag and \
                potential_state.inflow_der >= potential_state.outflow_der:
            if potential_state.vol_der <= state.vol_der:
                if not (potential_state.inflow_der == State.der_qs[1] and
                        potential_state.outflow_der == State.der_qs[1]):
                    return False

        if state.vol_der == State.der_qs[1]:
            if potential_state.inflow_der >= state.inflow_der and \
                potential_state.outflow_der <= state.outflow_der:
                if potential_state.vol_der < state.der_qs[1] and \
                    not potential_state.inflow_mag < potential_state.outflow_mag:
                    return False
            if potential_state.inflow_der <= state.inflow_der and \
                potential_state.outflow_der >= state.outflow_der:
                if potential_state.vol_der > state.der_qs[1] and \
                    not potential_state.inflow_mag > potential_state.outflow_mag:
                    return False
        return True

    @staticmethod
    def check_max_clipping(potential_state):
        # When the volume magnitude is max, the derivative should not be +.
        if potential_state.vol_mag == State.vol_qs[2] and potential_state.vol_der == State.der_qs[2]:
            return False
        # When the outflow magnitude is max, the derivative should not be +.
        if potential_state.outflow_mag == State.outflow_qs[2] and potential_state.outflow_der == State.der_qs[2]:
            return False
        return True

    @staticmethod
    def check_min_clipping(potential_state):
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
        # Apply the proportionality constraint on outflow and volume.
        if potential_state.outflow_der != potential_state.vol_der:
            return False
        return True

    @staticmethod
    def check_continuity(state, potential_state):
        # Apply continuity constraint on all the quantities.
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
        # Check the order of the exogenous inflow imposed.
        if state.inflow_der == State.der_qs[1] and potential_state.inflow_der == State.der_qs[2]:
            return False
        return True

    @staticmethod
    def check_value_constraint(potential_state):
        # Check the value constraints between volume and outflow.
        if (potential_state.vol_mag == State.vol_qs[0] or potential_state.vol_mag == State.vol_qs[2]) and potential_state.outflow_mag != potential_state.vol_mag:
            return False
        else:
            return True

    @staticmethod
    def check_simultaneous_change(state, potential_state):
        # Check simultaneous changes for both magnitudes and derivatives for the quantities (excluding extreme cases).
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
            # return False
            if not (potential_state.outflow_mag == State.outflow_qs[0] or
                    potential_state.outflow_mag == State.outflow_qs[2]):
                return False
        return True

    @staticmethod
    def check_point_values(state, potential_state):
        # Check transition from point values and the consistency w.r.t. their corresponding derivatives.
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
    def check_interval_values(state, potential_state):
        # Check transition from interval values and the consistency w.r.t. their corresponding derivatives.
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
        # Initialize variables.
        states = [self.scenario]
        visited_states = []
        parent_state = self.scenario
        counter = 1

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
                        State.check_interval_values(parent_state, potential_state):
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
        nodes = dict()
        for state in self.states:
            state_node = pydot.Node('State {}\nInflow({}, {})\nVolume({}, {})\nOutflow({}, {})'
                                    .format(state.id, State.str_mag_qs[state.inflow_mag], State.str_der_qs[state.inflow_der], State.str_mag_qs[state.vol_mag], State.str_der_qs[state.vol_der], State.str_mag_qs[state.outflow_mag], State.str_der_qs[state.outflow_der]),
                                    shape='box')
            nodes[state.id] = state_node
            self.graph.add_node(state_node)
            if state.id != 1:
                for parent_id in state.parent_ids:
                    self.graph.add_edge(pydot.Edge(nodes[parent_id], nodes[state.id], label=state.diff(self.states_dict[parent_id])))

    def output_graph(self):
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, 'result')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.graph.write_pdf(os.path.join(dirname, 'state_graph.pdf'))
