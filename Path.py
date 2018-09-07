
class Path:

    def __init__(self, type, change):

        self.__MOVE_TYPES = ['single_swap', 'single_change']

        if type in self.__MOVE_TYPES:
            self.type = type

        else:
            raise ValueError('Only types accepted are %s.' % (', '.join(MOVE_TYPES)))

        self.change = change
