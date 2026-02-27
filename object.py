class Player:
    def __init__(self, id, order, first, last, pos, ab, hits):
        self.id = id
        self.order = order
        self.first = first
        self.last = last
        self.pos = pos
        self.ab = ab
        self.hits = hits

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

    @property
    def avg(self):
        return round(self.hits / self.ab, 3) if self.ab else 0.0


class Lineup:
    def __init__(self):
        self.players = []

    def add(self, player):
        self.players.append(player)

    def remove(self, index):
        self.players.pop(index)

    def move(self, old, new):
        p = self.players.pop(old)
        self.players.insert(new, p)

    def get(self, index):
        return self.players[index]

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        return iter(self.players)
