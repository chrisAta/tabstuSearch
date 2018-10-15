
class Move:

    def __init__(self, old_sol, new_sol, path):
        self.old_sol = old_sol
        self.new_sol = new_sol
        self.path = path

    def __str__(self):
         return str(self.path.change)
