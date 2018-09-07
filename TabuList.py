from collections import deque

class TabuList:

    def __init__(self, list_len):
        self.tabu_list = deque(maxlen = list_len)

    def is_move_tabu(move):
        return move.path in self.tabu_list
