import random


class RandomAgent:
    def __init__(self, possible_actions: int):
        self._possible_actions = possible_actions

    def compute_single_action(self, state: dict, *args, **kwargs) -> tuple[int, None, None]:
        move = int(random.random() * self._possible_actions)
        while state['action_mask'][move] == 0:
            move = int(random.random() * self._possible_actions)

        return move, None, None