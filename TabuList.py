from Path import Path
from TabuTenure import TabuTenure
from collections import deque


class TabuList:

    def __init__(self, list_len, list_type, max_tenure):
        self._LISTTYPES = ['single', 'double', 'tuple']
        self.tabu_list = deque(maxlen = list_len)

        if list_type not in self._LISTTYPES:
            raise ValueError('Only types accepted are %s.' % (', '.join(self._LISTTYPES)))

        self.list_type = list_type
        self._max_tenure = max_tenure

    def is_move_tabu(self, move):
        return move.path in self.tabu_list

    def append_tabu_list(self, path):

        # if not isinstance(path, Path):

        print self.list_type

        if self.list_type == 'single':
            print path.change
            if not isinstance(path.change, list):
                raise ValueError('Tabu List Type is SINGLE - Path should be a list with a single element')

            if len(path.change) != 1:
                raise ValueError('Tabu List Type is SINGLE - Path should be a list with a single element')

            print 'Appending'
            self.tabu_list.append(TabuTenure(path.change, self._max_tenure, 0))

        elif self.list_type == 'double':
            if not isinstance(path.change, list):
                raise ValueError('Tabu List Type is DOUBLE - Path should be a list with two elements')

            if len(path.change != 2):
                raise ValueError('Tabu List Type is DOUBLE - Path should be a list with two elements')

            self.tabu_list.append(TabuTenure(path.change, self._max_tenure, 0))

        else:
            if not isinstance(path.change, tuple):
                raise ValueError('Tabu List Type is TUPLE - Path should be a tuple with two elements')

            if len(path.change !=2):
                raise ValueError('Tabu List Type is TUPLE - Path should be a tuple with two elements')

            self.tabu_list.append(TabuTenure(path.change, self._max_tenure, 0))


    def increment_tabu_tenure(self):
        for i in range(0, len(self.tabu_list)):
            self.tabu_list[i].curr_tenure += 1
