from game_manager import GameManager
from state import State
from constants import Consts
from node import Node
from screen_manager import Display
import time


def __main__():
    game_manager = GameManager()
    # Finding way
    result = game_manager.start_search('ids')

    # Putting path to goal in list
    result_list = []
    watchdog = 0
    while result is not None:
        watchdog += 1
        if watchdog > 1000:
            raise Exception('Watchdog limit exceeded')
        result_list.append(result.state)
        result = result.parent
    result_list.reverse()

    # Starting display
    display.update(init_state)
    display.begin_display()

    # Showing way
    if len(result_list) == 0:
        print('There is no way.')
        return
    for state in result_list:
        time.sleep(Consts.STEP_TIME)
        display.update(state)


__main__()
