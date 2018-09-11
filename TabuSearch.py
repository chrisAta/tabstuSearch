from TabuList import TabuList
from abc import abstractmethod
from numpy import argmax
from copy import deepcopy


class TabuSearch:

    def __init__(self, initial_solution, max_len, list_type, max_tenure, max_steps, max_score='*'):
        self.curr_sol = initial_solution
        self.tabu_list = TabuList(max_len, list_type, max_tenure)
        self.max_steps = max_steps
        self.best = ''
        self.max_score = max_score
        self.evaluate_curr_sol()
        # self.move_manager = MoveManager()

    @abstractmethod
    def _create_neighbourhood(self):
        """
            take self.curr_sol and produce a list of moves/paths
        """
        pass

    @abstractmethod
    def _score(self, val):
        pass

    def evaluate_curr_sol(self):
        self.curr_sol.fitness = self._score(self.curr_sol)

    def _best_score(self, neighbourhood):
        return neighbourhood[argmax([self._score(x.new_sol) for x in neighbourhood])]

    def run(self):
        for i in range(0, self.max_steps):

            neighbourhood = self._create_neighbourhood()
            neighbourhood_best = self._best_score(neighbourhood)

            self.tabu_list.remove_expired_tabus()

            while True:
                if self.tabu_list.is_move_tabu(neighbourhood_best):
                    if self._score(neighbourhood_best.new_sol) > self._score(self.best):
                        print 'ASPIRATION!'
                        self.tabu_list.append_tabu_list(neighbourhood_best.path)
                        self.best = deepcopy(neighbourhood_best.new_sol)
                        self.curr_sol = deepcopy(neighbourhood_best.new_sol)  # ??
                        break

                    else:
                        neighbourhood.remove(neighbourhood_best)
                        neighbourhood_best = self._best_score(neighbourhood)

                else:
                    self.tabu_list.append_tabu_list(neighbourhood_best.path)
                    self.curr_sol = deepcopy(neighbourhood_best.new_sol)
                    if self.best == '' or self._score(self.curr_sol) > self._score(self.best):
                        self.best = deepcopy(self.curr_sol)

                    break

            self.tabu_list.increment_tabu_tenure()

            if self.max_score != '*' and self._score(self.best) >= self.max_score:
                print 'REACHED MAX SCORE AFTER ' + str(i) + ' ITERATIONS'
                return self.best, self._score(self.best)

            # print self._score(self.curr_sol)

        print 'REACHED MAX STEPS'
        return self.best, self._score(self.best)
