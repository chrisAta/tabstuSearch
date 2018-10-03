from TabuList import TabuList
from abc import abstractmethod
from numpy import argmax
from copy import deepcopy


class TabuSearch:

    def __init__(self, initial_solution, max_len, list_type, max_tenure, max_steps, max_score='*', max_wait='*', opt_tuple=()):
        self.curr_sol = initial_solution
        self.tabu_list = TabuList(max_len, list_type, max_tenure)
        self.max_steps = max_steps
        self.best = ''
        self.max_score = max_score
        self.opt_tuple = opt_tuple
        self.max_wait = max_wait
        self.wait = 0
        self.evaluate_curr_sol()

    @abstractmethod
    def _create_neighbourhood(self):
        """
            take self.curr_sol and produce a list of moves/paths
        """
        pass

    @abstractmethod
    def _score(self, val):
        pass

    @abstractmethod
    def _post_swap_change(self, move):

        # still thinking about this method in case some post move
        # changes need to be made to something like eq 5 of the memetic algo
        # good place to use the optional tuple
        # for example, if it takes a move as parameter, you can do:
        #
        #
        # Obviously would do this in a loop or something but just to show
        # an example
        #  if i=0 and j=3 were swapped in the algo, then to emulate eq5, i in U and j in Z
        #
        # numpymatrix = self._opt_tuple[0]
        # delta = self._opt_tuple[1]
        # swap_indices = move.path.change
        # delta[0] = - delta[0] + numpymatrix[0,3]
        # delta[3] = - delta[3] + numpymatrix[0,3]
        # delta[1] = delta[1] + numpymatrix[0,1] - numpymatrix[1,3] if [1] in U
        # delta[2] = delta[2] - numpymatrix[0,2] = numpymatrix[1,2] of [2] in Z
        # etc
        #

        pass


    def evaluate_curr_sol(self):
        self.curr_sol.fitness = self._score(self.curr_sol)

    def _best_score(self, neighbourhood):
        return neighbourhood[argmax([self._score(x.new_sol) for x in neighbourhood])]

    def run(self):
        for i in range(0, self.max_steps):

            # print i

            neighbourhood = self._create_neighbourhood()
            neighbourhood_best = self._best_score(neighbourhood)

            self.tabu_list.remove_expired_tabus()

            while True:

                if self.tabu_list.is_move_tabu(neighbourhood_best):
                    if self._score(neighbourhood_best.new_sol) >= self._score(self.best):
                        print 'ASPIRATION!'
                        self.tabu_list.append_tabu_list(neighbourhood_best.path)
                        self.best = deepcopy(neighbourhood_best.new_sol)
                        self.curr_sol = deepcopy(neighbourhood_best.new_sol)  # ??

                        if self.max_wait !='*':
                            self.wait = 0

                        print self.best.fitness
                        break

                    else:
                        print len(neighbourhood)
                        neighbourhood.remove(neighbourhood_best)
                        neighbourhood_best = self._best_score(neighbourhood)

                else:
                    self.tabu_list.append_tabu_list(neighbourhood_best.path)
                    self.curr_sol = deepcopy(neighbourhood_best.new_sol)
                    print self.curr_sol.fitness
                    # print self.tabu_list.element_list
                    if self.best == '' or self._score(self.curr_sol) >= self._score(self.best):
                        self.best = deepcopy(self.curr_sol)

                        if self.max_wait !='*':
                            self.wait = 0

                        print 'NEW BEST'
                        print self.best.fitness

                    elif self.max_wait !='*':
                        self.wait += 1


                    break

            self.tabu_list.increment_tabu_tenure()

            # print self.curr_sol.fitness

            # call abstract post_swap_change method in case necessary for algo (like eq5 for memetic algo paper)
            # _post_swap_change(neighbourhood_best)
            if self.max_score != '*' and self._score(self.best) >= self.max_score:
                print 'REACHED MAX SCORE AFTER ' + str(i) + ' ITERATIONS'
                return self.best, self._score(self.best)


            if self.max_wait !='*' and self.wait == self.max_wait:
                print str(self.max_wait) + ' ITERATATIONS WITHOUT IMPROVEMENT, STOPPING'
                return self.best, self._score(self.best)

            # print self._score(self.curr_sol)
            # print self._score(self.best)

        print 'REACHED MAX STEPS'
        return self.best, self._score(self.best)
