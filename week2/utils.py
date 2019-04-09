

class State:

    def __init__(self, state_id, inflow_mag, inflow_der, outflow_mag, outflow_der, vol_mag, vol_der):
        self.id = state_id
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
