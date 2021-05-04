#!/usr/bin/env python3

from game_manager import GameManager
import sys


def __main__():
    arg = sys.argv
    search_type = 'bd_bfs'
    if len(arg) > 1:
        if arg[1] in ['ids', 'a_start', 'bd_bfs']:
            search_type = arg[1]
        else:
            print('\n\nUse "ids" or "a_star" or "bd_bfs" as argument.')
            return
    game_manager = GameManager()
    # Finding way
    game_manager.start_search(search_type)


__main__()
