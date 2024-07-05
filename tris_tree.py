import time

import numpy as np
from networkx import DiGraph
import copy
from state import TrisState


def __generate_sons__(state: TrisState, node_type: str, alpha=None, beta=None):
    list_neighbors = []

    for r in range(3):
        for c in range(3):
            if state.get_cell(r, c) != 'X' and state.get_cell(r, c) != 'O':
                copied_state = copy.deepcopy(state)
                copied_state.add_move(node_type, r, c)
                if alpha is not None:
                    copied_state.alpha = alpha
                if beta is not None:
                    copied_state.beta = beta
                list_neighbors.append(copied_state)

    return list_neighbors


def __generate_graph__(graph: DiGraph, current_state: TrisState, player: str, depth: int, alpha: int = -float('inf'), beta: int = float('inf')):
    graph.add_node(current_state, label=player)
    sons = __generate_sons__(current_state, player, alpha, beta)

    list_utility = []
    if player == 'max':
        max_eval = -float('inf')
        for node in sons:
            graph.add_edge(current_state, node)
            state = node.get_state()
            if state == 'NF':
                eval = __generate_graph__(graph, node, 'min', depth + 1, alpha, beta)
                max_eval = max(max_eval, eval)
                current_state.alpha = max(current_state.alpha, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            elif state == "W":
                eval = 10 - depth
                max_eval = max(max_eval, eval)
                graph.nodes[node]['weight'] = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            elif state == "L":
                eval = -1
                max_eval = max(max_eval, eval)
                graph.nodes[node]['weight'] = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            elif state == "D":
                eval = 0
                max_eval = max(max_eval, eval)
                graph.nodes[node]['weight'] = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            else:
                raise Exception("Spero che questa eccezione non accada mai :)")
            list_utility.append(eval)
        utility = max_eval
    else:
        min_eval = float('inf')
        for node in sons:
            graph.add_edge(current_state, node)
            state = node.get_state()
            if state == 'NF':
                eval = __generate_graph__(graph, node, 'max', depth + 1, alpha, beta)
                min_eval = min(min_eval, eval)
                current_state.beta = min(current_state.beta, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            elif state == "W":
                eval = 10 - depth
                min_eval = min(min_eval, eval)
                graph.nodes[node]['weight'] = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            elif state == "L":
                eval = -1
                min_eval = min(min_eval, eval)
                graph.nodes[node]['weight'] = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            elif state == "D":
                eval = 0
                min_eval = min(min_eval, eval)
                graph.nodes[node]['weight'] = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            else:
                raise Exception("Spero che questa eccezione non accada mai :)")
            list_utility.append(eval)
        utility = min_eval

    graph.nodes[current_state]['weight'] = utility
    return utility


class TrisTree:
    """
    If starter = True means that the other players should start
    """

    def __init__(self, initial_state=None):
        super().__init__()
        self.graph = DiGraph()

        if initial_state is None:
            self.current_state = TrisState()
        else:
            """
            if not isinstance(initial_state, list) or not all(
                    isinstance(row, list) and all(isinstance(cell, str) for cell in row) for row in initial_state):
                raise Exception("Bad type initial state")""" # TODO fix this section
            self.current_state = TrisState(initial_state)

        __generate_graph__(self.graph, self.current_state, 'max', depth=0)

    def get_best_move(self) -> TrisState:
        if self.graph.nodes[self.current_state]['label'] == 'min':
            raise Exception("I have to wait for the opponent move")

        possible_moves = list(self.graph.neighbors(self.current_state))
        list_utility = list(map(lambda x: self.graph.nodes[x]['weight'], possible_moves))
        max_utility = max(list_utility)
        self.current_state = possible_moves[list_utility.index(max_utility)]
        return copy.deepcopy(self.current_state)


    def opponent_move(self, row, col) -> TrisState:
        new_state = copy.deepcopy(self.current_state)
        new_state.add_move('min', row, col)

        self.graph.clear()
        self.current_state = new_state
        __generate_graph__(self.graph, self.current_state, 'max', depth=0)

        return new_state


    def reset_tree(self):
        self.graph.clear()
        self.current_state = TrisState()
        __generate_graph__(self.graph, self.current_state, 'max', depth=0)


if __name__ == '__main__':
    tt = TrisTree(np.array([["X", "", ""],
                                      ["", "", ""],
                                      ["", "", ""]]))

    print(tt.get_best_move())

    print(tt.opponent_move(2,1))

    print(tt.get_best_move())

    tt.reset_tree()

    print(tt.get_best_move())