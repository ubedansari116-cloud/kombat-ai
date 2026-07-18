from copy import deepcopy


class WhatIfSimulator:

    def simulate(
        self,
        fight_engine,
        fighter_one_name,
        fighter_one_stats,
        fighter_two_name,
        fighter_two_stats,
        fighter_one_changes=None,
        fighter_two_changes=None,
    ):

        first = deepcopy(fighter_one_stats)
        second = deepcopy(fighter_two_stats)

        if fighter_one_changes:
            first.update(fighter_one_changes)

        if fighter_two_changes:
            second.update(fighter_two_changes)

        print("\n====================")
        print(first)
        print("====================")
        print(second)
        print("====================")

        return fight_engine.analyze(
            fighter_one_name=fighter_one_name,
            fighter_one_stats=first,
            fighter_two_name=fighter_two_name,
            fighter_two_stats=second,
        )