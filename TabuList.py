from Path import Path
from TabuTenure import TabuTenure
from collections import deque


class TabuList:

    def __init__(self, list_len, list_type, max_tenure):
        self._LISTTYPES = ['single', 'double', 'tuple']
        self.tabu_list = deque(maxlen=list_len)
        self.element_list = deque(maxlen=list_len)

        if list_type not in self._LISTTYPES:
            raise ValueError('Only types accepted are %s.' % (', '.join(self._LISTTYPES)))

        self.list_type = list_type
        self._max_tenure = max_tenure

    def is_move_tabu(self, move):

        if len(self.element_list) == 0:
            return False

        if self.list_type in ('single'):
            return move.path.change[0] in self.element_list

        if self.list_type == 'double':
            # temp = [x for sub in self.element_list for x in sub]
            # print temp
            # print move.path.change
            # print self.element_list
            return True in [x in self.element_list for x in move.path.change]

        if self.list_type in ('tuple'):
            return move.path.change in self.element_list


    def append_tabu_list(self, path):

        # if not isinstance(path, Path):

        # temp = [x for sub in self.element_list for x in sub]

        if path.change in self.element_list:
            copy = list(self.tabu_list)

            for i in range(0, len(copy)):
                if copy[i].element == path.change:
                    self.tabu_list[i].curr_tenure = 0
                    return

        if self.list_type == 'single':
            if not isinstance(path.change, list):
                raise ValueError('Tabu List Type is SINGLE - Path should be a list with a single element')

            if len(path.change) != 1:
                raise ValueError('Tabu List Type is SINGLE - Path should be a list with a single element')

            self.tabu_list.append(TabuTenure(path.change[0], self._max_tenure, 0))
            self.element_list.append(path.change[0])

        elif self.list_type == 'double':
            if not isinstance(path.change, list):
                raise ValueError('Tabu List Type is DOUBLE - Path should be a list with two elements')

            if len(path.change) != 2:
                raise ValueError('Tabu List Type is DOUBLE - Path should be a list with two elements')


            # HAVE TO RESET THE TENURE IF IT ALREADY EXISTS AND GETS TABU AGAIN
            self.tabu_list.append(TabuTenure(path.change[0], self._max_tenure, 0))
            self.tabu_list.append(TabuTenure(path.change[1], self._max_tenure, 0))
            self.element_list.append(path.change[0])
            self.element_list.append(path.change[1])


            # if path.change[0] not in self.element_list
            #
            # self.element_list.append(path.change)

        else:
            if not isinstance(path.change, tuple):
                raise ValueError('Tabu List Type is TUPLE - Path should be a tuple with two elements')

            if len(path.change !=2):
                raise ValueError('Tabu List Type is TUPLE - Path should be a tuple with two elements')

            self.tabu_list.append(TabuTenure(path.change, self._max_tenure, 0))
            self.element_list.append(path.change)


    def increment_tabu_tenure(self):
        for i in range(0, len(self.tabu_list)):
            self.tabu_list[i].curr_tenure += 1

    def remove_expired_tabus(self):
        copy = list(self.tabu_list)
        for tabu in copy:
            if tabu.curr_tenure > self._max_tenure:
                self.tabu_list.remove(tabu)
                self.element_list.remove(tabu.element)
