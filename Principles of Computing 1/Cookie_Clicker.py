"""
Cookie Clicker Simulator
http://www.codeskulptor.org/#user45_GncSECR0xj_1.py
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
#SIM_TIME = 10000000000.0
SIM_TIME = 5000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies_produced = 0.0
        self._current_cookies = 0.0
        self._game_time = 0.0
        self._cps = 1.0

        #[time, item bought at time, item cost, total cookies]
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        print
        print "Total Cookies:   ", self._total_cookies_produced
        print "Current Cookies: ", self._current_cookies
        print "Game Time:       ", self._game_time
        print "CPS:             ", self._cps
        print
        print "History:         ", self._history

        return ""

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._game_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        # use // or int?
        if cookies - self._current_cookies <= 0:
            return 0.0
        else:
            return (cookies - self._current_cookies) / self._cps

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0:
            return
        else:
            self._total_cookies_produced += time * self._cps
            self._current_cookies += time * self._cps
            self._game_time += time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies < cost:
            return False
        else:
            self._current_cookies -= cost			#subtract cost
            self._cps += additional_cps 			#add cps
            self._history.append(tuple([self._game_time,
                                item_name,
                                cost,
                                self._total_cookies_produced]))
            return True

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    build_info_clone = build_info.clone()
    new_game = ClickerState()
    item_name = ""

    while new_game.get_time() <= duration:
        if new_game.get_time() > duration:
            break
        else:
            item_name = strategy(new_game.get_cookies(),
                                 new_game.get_cps(),
                                 new_game.get_history(),
                                 duration - new_game.get_time(),
                                 build_info_clone)
        if item_name == None:
            break
        time_to_buy = math.ceil(
            (build_info_clone.get_cost(item_name) - new_game.get_cookies())
            / new_game.get_cps())
        if time_to_buy + new_game.get_time() <= duration:
            new_game.wait(time_to_buy)
            if (new_game.buy_item(item_name,
                                  build_info_clone.get_cost(item_name),
                                  build_info.get_cps(item_name))):
                build_info_clone.update_item(item_name)
        else:
            break

    new_game.wait(duration - new_game.get_time())
    return new_game

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """

    build_list = build_info.build_items()
    min_cost = float("Inf")
    for build_item in build_list:
        build_cost = build_info.get_cost(build_item)
        if build_cost < min_cost:
            min_cost = build_cost
            min_build = build_item

    if (cookies + time_left * cps) < min_cost:
        return None
    else:
        return min_build

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """

    build_list = build_info.build_items()
    build_item_cost = dict()
    for build_item in build_list:
        build_item_cost[build_info.get_cost(build_item)] = build_item

    build_item_cost_list = build_item_cost.keys()
    build_item_cost_list.sort(reverse = True)

    for cost in build_item_cost_list:
        if cost <= (cookies + time_left * cps):
            return build_item_cost.get(cost)
    return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    build_list = build_info.build_items()
    build_item_cps_cost_ratio = dict()
    for build_item in build_list:
        build_item_cps_cost_ratio[build_info.get_cps(build_item) /
                                   build_info.get_cost(build_item)] = build_item

    build_item_cps_cost_ratio_list = build_item_cps_cost_ratio.keys()
    build_item_cps_cost_ratio_list.sort(reverse = True)

    for cps_cost_ratio in build_item_cps_cost_ratio_list:
        build_item = build_item_cps_cost_ratio.get(cps_cost_ratio)
        cost = build_info.get_cost(build_item)
        if cost <= (cookies + time_left * cps):
            return build_item

    return None


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    run_strategy("None", SIM_TIME, strategy_none)
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)

#run()

def test():
    """
    tests
    The first three test ClickerState
    """

    obj_1 = ClickerState()
    obj_1.wait(78.0)
    obj_1.buy_item('item', 1.0, 1.0)
    obj_1.time_until(22.0)
    print obj_1
    #expected 0.0 but received -27.5

    obj_2 = ClickerState()
    obj_2.wait(45.0)
    obj_2.buy_item('item', 1.0, 3.5)
    print obj_2
    #expected obj: Time: 45.0 Current Cookies: 44.0 CPS: 4.5 Total Cookies: 45.0 History (length: 2): [(0.0, None, 0.0, 0.0), (45.0, 'item', 1.0, 45.0)] but received (printed using your __str__ method)  Expected a <type 'tuple'>  (45.0, 'item', 1.0, 45.0) but received <type 'list'>  [45.0, None, 0.0, 45.0]

    obj_3 = ClickerState()
    obj_3.wait(1.0)
    print obj_3
    #expected obj: Time: 1.0 Current Cookies: 1.0 CPS: 1.0 Total Cookies: 1.0 History (length: 1): [(0.0, None, 0.0, 0.0)] but received (printed using your __str__ method)  (Exception: Length Error) When comparing against [(0.0, None, 0.0, 0.0)] (1 elements), the value, [(0.0, None, 0.0, 0.0), [1.0, None, 0.0, 1.0]] (2 elements) has too many elements.

#test()

def test2():
    """
    more tests
    """
    state = simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.1]}, 1.15),
                     5000.0,
                     strategy_none)
    print state
test2()
