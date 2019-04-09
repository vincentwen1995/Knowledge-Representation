

class State:
    der_qs = (-1, 0, 1)
    inflow_qs = (0, 1)
    outflow_qs = (0, 1, 2)
    vol_qs = (0, 1, 2)

    def __init__(self, id, parent_id, inflow_mag, inflow_der, outflow_mag, outflow_der, vol_mag, vol_der):
        self.id = id
        self.parent_id = parent_id
        self.inflow_mag = inflow_mag
        self.inflow_der = inflow_der
        self.outflow_mag = outflow_mag
        self.outflow_der = outflow_der
        self.vol_mag = vol_mag
        self.vol_der = vol_der

    def __str__(self):
        return 'State id: {}\n'.format(self.id) \
            + 'Inflow Magnitude: {}\n'.format(self.inflow_mag) \
            + 'Inflow Derivative: {}\n'.format(self.inflow_der) \
            + 'Outflow Magnitude: {}\n'.format(self.outflow_mag) \
            + 'Outflow Derivative: {}\n'.format(self.outflow_der) \
            + 'Volume Magnitude: {}\n'.format(self.vol_mag) \
            + 'Volume Derivative: {}\n'.format(self.vol_der)

    def __eq__(self, other):
        return self.inflow_mag == other.inflow_mag and \
            self.inflow_der == other.inflow_der and \
            self.outflow_mag == other.outflow_der and \
            self.outflow_der == other.outflow_der and \
            self.vol_mag == other.vol_mag and \
            self.vol_der == other.vol_der

    @staticmethod
    def propagate_inflow_mag(state: State):
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
    def propagate_vol_der(state: State):
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
        return vol_ders

    @staticmethod
    def propagate_vol_mag(state: State):
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

        return vol_mags

    @staticmethod
    def propagate_outflow_der(state: State):
        '''Use the proportionality P+(volume, outflow)
        to propagate the derivative of the outflow.

        Returns:
            [int]: possible values for the outflow derivative
        '''

        outflow_ders = []
        outflow_ders.append(state.vol_der)
        return outflow_ders

    @staticmethod
    def propagate_outflow_mag(state: State):
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


class Flow:

    def __init__(self, scenario):
        self.scenario = scenario

    