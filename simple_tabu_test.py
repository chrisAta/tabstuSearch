from TabuSearch import TabuSearch
from Move import Move
from Path import Path
from Solution import Solution
from copy import deepcopy
from random import choice, randint, random
from string import ascii_lowercase


class SimpleTest(TabuSearch):

    def _create_neighbourhood(self):
        curr_sol = self.curr_sol
        neighbourhood = []

        for i in range(0, 30):
            neighbour = deepcopy(curr_sol)
            rand_num = randint(0, 94)
            temp_val = list(neighbour.val)
            temp_val[rand_num] = choice(ascii_lowercase)
            neighbour.val = ''.join(temp_val)
            neighbour.fitness = self._score(neighbour)
            path = Path('single_change', [rand_num])
            move = Move(curr_sol, neighbour, path)
            neighbourhood.append(move)

        return neighbourhood

    def _score(self, sol):
        return float(sum(sol.val[i] == "thetroutisbeautifulthetroutisbeautifulthetroutisbeautifulthetroutisbeautifulthetroutisbeautiful"[i] for i in range(95)))


def main():

    ini_sol = Solution('abcdeabcdeabcdeabcdabcdeabcdeabcdeabcdabcdeabcdeabcdeabcdabcdeabcdeabcdeabcdabcdeabcdeabcdeabcd')
    test = SimpleTest(ini_sol, 50, 'single', 20, 50000, 95.0)

    best, score = test.run()

    print best.val
    print score

if __name__ == "__main__":
    main()
