# !/usr/bin/env python3
# coding: utf-8

import itertools
import random

import numpy as np


# convert a list of int into string
# e.g. [1,1,1] -> "111"
def num_list_to_str(num_list):
    return "".join(str(e) for e in num_list)


# Select best item in list. If has several best one:
# Choose from them randomly
def max_randomly(list_item, key_function):
    list_item.sort(key=key_function, reverse=True)
    item_iter = 0
    second_item_index = len(list_item) - 1
    max_key = key_function(list_item[0])
    for item in list_item:
        if key_function(item) < max_key:
            second_item_index = item_iter
        item_iter += 1
    return list_item[random.randint(0, second_item_index - 1)]


class StrategyTable(object):
    def __init__(self, depth=3):
        """
        :param depth: agent memory
        :return: None
        """

        combinations_string_list = [num_list_to_str(i) for i in itertools.product([0, 1], repeat=depth)]
        self.__strategy_table = {x: random.randint(0, 1) for x in combinations_string_list}
        self.__weight = 0

    @property
    def weight(self):
        return self.__weight

    @property
    def strategy_table(self):
        return self.__strategy_table

    # predict with a string format history input
    def predict(self, history):
        """
        :param history: past m winning groups
        :return: next decision
        """
        return self.__strategy_table[history]

    def update_weight(self, is_win):
        """
        :param is_win: boolean, Did the strategy win
        :return: adjust the weight
        """
        if is_win:
            self.__weight += 1
        else:
            self.__weight -= 1


class Agent(object):
    """
    base class for AgentWithStrategyTable
    Also, used in random simulation
    """

    def random_predict(self):
        return random.randint(0, 1)


class AgentWithStrategyTable(Agent):
    """
    composed with StrategyTable class
    inherited with Agent class
    """

    def __init__(self, depth=3, strategy_num=2):
        # last memory
        self.__history = None
        self.__depth = depth
        # init strategy_pool
        self.__strategy_pool = []
        for x in range(strategy_num):
            self.__strategy_pool.append(StrategyTable(depth))

    @property
    def strategy_pool(self):
        return self.__strategy_pool

    # predict with memory, a list
    def predict(self, history):
        """
        :param history: last m winning group code, list of int
        :return:   next decision from a table which has the highest weight
        """
        history = num_list_to_str(history)
        if len(history) == self.__depth:
            self.__history = history
            strategy_choice = max_randomly(self.__strategy_pool, lambda x: x.weight)
            return strategy_choice.predict(self.__history)
        else:
            raise Exception("agent memory input error")

    # result is winner room number
    # update weights of tables
    def get_winner(self, result):
        """
        :param result: the winning group of this round
        """
        for table in self.__strategy_pool:
            is_win = result == table.predict(self.__history)
            table.update_weight(is_win)


class MinorityGame(object):
    """
    a base class for minority Game
    """
    def __init__(self, agent_num, run_num):
        self.agent_num = agent_num
        self.run_num = run_num
        self.agent_pool = []
        self.win_history = np.zeros(run_num)

    @property
    def score_mean_std(self):
        """
        :return: the winner number mean and stdd
        """
        return self.win_history.mean(), self.win_history.std()

class MinorityGameWithRandomChoice(MinorityGame):
    """
    a Class for random choice Minority Game
    """
    def __init__(self, agent_num, run_num):
        super().__init__(agent_num, run_num)
        for i in range(self.agent_num):
            self.agent_pool.append(Agent())

    def run_game(self):
        


class MinorityGameWithStrategyTable(MinorityGame):
    """
    class used for run the minority game with StrategyTable
    """
    def __init__(self, agent_num, run_num, depth, *strategy_num):
        super().__init__(agent_num, run_num)
        self.all_history = list()
        self.depth = depth
        self.strategy_num = strategy_num

        for x in range(depth):
            self.all_history.append(random.randint(0, 1))

    def init_agents(self):
        """
        generate S tables for each agent
        if strategy_num has multiple variable, then the agent population will have
        different  strategy number for each agent
        """
        for i in range(self.agent_num):
            if i < self.agent_num // len(self.strategy_num):
                self.agent_pool.append(AgentWithStrategyTable(self.depth, self.strategy_num[0]))
            else:
                self.agent_pool[i].append(AgentWithStrategyTable(self.depth, self.strategy_num[1]))

    def run_game(self):
        """
        run the minority game n times
        """
        for i in range(self.run_num):
            num_of_one = 0
            for agent in self.agent_pool:
                num_of_one += agent.predict(self.all_history[-3:])
            game_result = 1 if num_of_one < self.agent_num / 2 else 0
            for agent in self.agent_pool:
                agent.get_winner(game_result)
            winner_num = num_of_one if game_result == 1 else self.agent_num - num_of_one
            self.win_history[i] = winner_num
            print("This is %dth Run" % i)


if __name__ == "__main__":
    m = MinorityGameWithStrategyTable(201, 500, 3, 5)
    m.init_agents()
    m.run_game()
    print(m.win_history)
