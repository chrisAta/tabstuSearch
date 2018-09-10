from TabuList import TabuList

class TabuSearch:

    def __init__(self, initial_solution, max_len, list_type, max_tenure):
        self.curr_sol = initial_solution
        self.tabu_list = TabuList(max_len, list_type, max_tenure)
        # self.move_manager = MoveManager()


    # create_neighbourhood()
    # score()
    # best_score()
    # run()
