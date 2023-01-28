
class Game:
    def __init__(self, id, *args):
        self.id = id
        self.tables = list(args)

    def get_id(self):
        return self.id

    def add_table(self, table):
        return self.tables.append(table)