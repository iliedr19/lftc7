class CanonicalCollection:
    def __init__(self):
        self.states = []
        self.adjacency_list = {}

    def connect_states(self, index_first_state, symbol, index_second_state):
        self.adjacency_list[(index_first_state, symbol)] = index_second_state

    def add_state(self, state):
        self.states.append(state)

    def get_states(self):
        return self.states

    def get_adjacency_list(self):
        return self.adjacency_list
