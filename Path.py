
class Path:

    def __init__(self, movetype, change):

        self._MOVETYPES = ['single_swap', 'single_change']
        self.change = change

        if movetype in self._MOVETYPES:
            self.movetype = movetype

        else:
            raise ValueError('Only types accepted are %s.' % (', '.join(self._MOVETYPES)))
