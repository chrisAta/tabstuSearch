from TabuList import TabuList
from abc import abstractmethod


class TabuSearch:

    def __init__(self, initial_solution, max_len, list_type, max_tenure, max_steps):
        self.curr_sol = initial_solution
        self.tabu_list = TabuList(max_len, list_type, max_tenure)
        self.max_steps = max_steps
        self.best = ''
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

        self.curr_sol.fitness = self._score(self.curr_sol.val)

    def _best_score(self, neighbourhood):
        return neighbourhood[argmax([self._score(x) for x in neighbourhood])]

    def run(self):
        for i in range(0, self.max_steps):
            neighbourhood = self._create_neighbourhood()
            neighbourhood_best = self._best_score(neighbourhood)

            while True:
                if self.tabu_list.is_move_tabu(neighbourhood_best):
                    if self._score(neighbourhood_best) > self._score(self.best):
                        self.tabu_list.append_tabu_list(neighborhood_best)
                        self.best = neighbourhood_best
                        self.curr_sol = neighborhood_best  # ??
                        break

                    else:
                        neighbourhood.remove(neighbourhood_best)
                        neighbourhood_best = self._best_score(neighbourhood)

                else:
                    self.tabu_list.append_tabu_list(neighbourhood_best)
                    self.curr_sol = neighbourhood_best
                    if self._score(self.current) > self._score(self.best):
                        self.best = self.current

                    break

            self.tabu_list.increment_tabu_tenure

        print 'RECHED MAX STEPS'
        return self.best, self._score(self.best)
