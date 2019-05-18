class Player:
    def __init__(self, id):
        self.id = id

    def do_move(self):
        raise NotImplementedError