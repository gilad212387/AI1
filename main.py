from framework import *
from deliveries import *

from matplotlib import pyplot as plt
import numpy as np
from typing import List, Union

# Load the map
roads = load_map_from_csv(Consts.get_data_file_path("tlv.csv"))

# Make `np.random` behave deterministic.
Consts.set_seed()


# --------------------------------------------------------------------
# -------------------------- Map Problem -----------------------------
# --------------------------------------------------------------------

def plot_distance_and_expanded_wrt_weight_figure(
        weights: Union[np.ndarray, List[float]],
        total_distance: Union[np.ndarray, List[float]],
        total_expanded: Union[np.ndarray, List[int]]):
    """
    Use `matplotlib` to generate a figure of the distance & #expanded-nodes
     w.r.t. the weight.
    """
    assert len(weights) == len(total_distance) == len(total_expanded)

    fig, ax1 = plt.subplots()

    # TODO: Plot the total distances with ax1. Use `ax1.plot(...)`.
    # TODO: Make this curve colored blue with solid line style.
    # See documentation here:
    # https://matplotlib.org/2.0.0/api/_as_gen/matplotlib.axes.Axes.plot.html
    # You can also search google for additional examples.

    ax1.plot(weights, total_distance, 'b-')

    # ax1: Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('distance traveled', color='b')
    ax1.tick_params('y', colors='b')
    ax1.set_xlabel('weight')

    # Create another axis for the #expanded curve.
    ax2 = ax1.twinx()

    # TODO: Plot the total expanded with ax2. Use `ax2.plot(...)`.
    # TODO: ax2: Make the y-axis label, ticks and tick labels match the line color.
    # TODO: Make this curve colored red with solid line style.

    ax2.plot(weights, total_expanded, 'r-')

    ax2.set_ylabel('states expanded', color='r')
    ax2.tick_params('y', colors='r')
    ax2.set_xlabel('weight')

    fig.tight_layout()
    plt.show()


def run_astar_for_weights_in_range(heuristic_type: HeuristicFunctionType, problem: GraphProblem):
    # TODO:
    # 1. Create an array of 20 numbers equally spreaded in [0.5, 1]
    #    (including the edges). You can use `np.linspace()` for that.
    # 2. For each weight in that array run the A* algorithm, with the
    #    given `heuristic_type` over the map problem. For each such run,
    #    store the cost of the solution (res.final_search_node.cost)
    #    and the number of expanded states (res.nr_expanded_states).
    #    Store these in 2 lists (array for the costs and array for
    #    the #expanded.
    # Call the function `plot_distance_and_expanded_by_weight_figure()`
    #  with that data.

    costs = []
    expanded_states_num = []
    for w in np.linspace(0.5, 1, 20):
        a_star = AStar(heuristic_type, w)
        res = a_star.solve_problem(problem)
        costs.append(res.final_search_node.cost)
        expanded_states_num.append(res.nr_expanded_states)

    plot_distance_and_expanded_wrt_weight_figure(np.linspace(0.5, 1, 20), costs, expanded_states_num)


def map_problem():
    print()
    print('Solve the map problem.')

    # Ex.8
    map_prob = MapProblem(roads, 54, 549)
    uc = UniformCost()
    res = uc.solve_problem(map_prob)
    print(res)

    # Ex.10
    # TODO: create an instance of `AStar` with the `NullHeuristic`,
    #       solve the same `map_prob` with it and print the results (as before).
    # Notice: AStar constructor receives the heuristic *type* (ex: `MyHeuristicClass`),
    #         and not an instance of the heuristic (eg: not `MyHeuristicClass()`).

    map_prob = MapProblem(roads, 54, 549)
    a_star = AStar(NullHeuristic)
    res = a_star.solve_problem(map_prob)
    print(res)

    # Ex.11
    # TODO: create an instance of `AStar` with the `AirDistHeuristic`,
    #       solve the same `map_prob` with it and print the results (as before).

    map_prob = MapProblem(roads, 54, 549)
    a_star = AStar(AirDistHeuristic)
    res = a_star.solve_problem(map_prob)
    print(res)

    # Ex.12
    # TODO:
    # 1. Complete the implementation of the function
    #    `run_astar_for_weights_in_range()` (upper in this file).
    # 2. Complete the implementation of the function
    #    `plot_distance_and_expanded_by_weight_figure()`
    #    (upper in this file).
    # 3. Call here the function `run_astar_for_weights_in_range()`
    #    with `AirDistHeuristic` and `map_prob`.

    map_prob = MapProblem(roads, 54, 549)
    run_astar_for_weights_in_range(AirDistHeuristic, map_prob)


# --------------------------------------------------------------------
# ----------------------- Deliveries Problem -------------------------
# --------------------------------------------------------------------

def relaxed_deliveries_problem():

    print()
    print('Solve the relaxed deliveries problem.')

    big_delivery = DeliveriesProblemInput.load_from_file('big_delivery.in', roads)
    big_deliveries_prob = RelaxedDeliveriesProblem(big_delivery)

    # Ex.16
    # TODO: create an instance of `AStar` with the `MaxAirDistHeuristic`,
    #       solve the `big_deliveries_prob` with it and print the results (as before).

    a_star = AStar(MaxAirDistHeuristic, 0.5)
    res = a_star.solve_problem(big_deliveries_prob)
    print(res)

    # Ex.17
    # TODO: create an instance of `AStar` with the `MSTAirDistHeuristic`,
    #       solve the `big_deliveries_prob` with it and print the results (as before).
    a_star = AStar(MSTAirDistHeuristic)
    res = a_star.solve_problem(big_deliveries_prob)
    print(res)

    # Ex.18
    # TODO: Call here the function `run_astar_for_weights_in_range()`
    #       with `MSTAirDistHeuristic` and `big_deliveries_prob`.
    run_astar_for_weights_in_range(MSTAirDistHeuristic, big_deliveries_prob)

    # Ex.24
    # TODO:
    # 1. Run the stochastic greedy algorithm for 100 times.
    #    For each run, store the cost of the found solution.
    #    Store these costs in a list.
    # 2. The "Anytime Greedy Stochastic Algorithm" runs the greedy
    #    greedy stochastic for N times, and after each iteration
    #    stores the best solution found so far. It means that after
    #    iteration #i, the cost of the solution found by the anytime
    #    algorithm is the MINIMUM among the costs of the solutions
    #    found in iterations {1,...,i}. Calculate the costs of the
    #    anytime algorithm wrt the #iteration and store them in a list.
    # 3. Calculate and store the cost of the solution received by
    #    the A* algorithm (with w=0.5).
    # 4. Calculate and store the cost of the solution received by
    #    the deterministic greedy algorithm (A* with w=1).
    # 5. Plot a figure with the costs (y-axis) wrt the #iteration
    #    (x-axis). Of course that the costs of A*, and deterministic
    #    greedy are not dependent with the iteration number, so
    #    these two should be represented by horizontal lines.

    greedy_stochastic = GreedyStochastic(MSTAirDistHeuristic)
    first_100 = []
    any_time_arr = []
    res_cost = greedy_stochastic.solve_problem(big_deliveries_prob).final_search_node.cost
    temp_min = res_cost
    first_100.append(res_cost)
    any_time_arr.append(res_cost)
    for i in range(99):
        temp_res_cost = greedy_stochastic.solve_problem(big_deliveries_prob).final_search_node.cost
        temp_min = min(temp_min, temp_res_cost)
        any_time_arr.append(temp_min)
        first_100.append(temp_res_cost)

    a_star_res = (AStar(MSTAirDistHeuristic)).solve_problem(big_deliveries_prob)
    greedy_best_first_res = (AStar(MSTAirDistHeuristic, 1)).solve_problem(big_deliveries_prob)

    fig, ax1 = plt.subplots()

    a_star_res_arr = []
    greedy_best_first_res_arr = []
    for _ in range(100):
        a_star_res_arr.append(a_star_res.final_search_node.cost)
        greedy_best_first_res_arr.append(greedy_best_first_res.final_search_node.cost)

    ax1.plot(range(100), first_100, 'b-')
    ax1.plot(range(100), any_time_arr, 'r-')
    ax1.plot(range(100), a_star_res_arr, 'g-')
    ax1.plot(range(100), greedy_best_first_res_arr, 'y-')

    plt.xlabel("iteration")
    plt.ylabel("costs")
    plt.grid()
    fig.tight_layout()
    plt.show()



def strict_deliveries_problem():
    print()
    print('Solve the strict deliveries problem.')

    small_delivery = DeliveriesProblemInput.load_from_file('small_delivery.in', roads)
    small_deliveries_strict_problem = StrictDeliveriesProblem(
        small_delivery, roads, inner_problem_solver=AStar(AirDistHeuristic))

    # Ex.26
    # TODO: Call here the function `run_astar_for_weights_in_range()`
    #       with `MSTAirDistHeuristic` and `big_deliveries_prob`.

    small_deliveries_prob = StrictDeliveriesProblem(problem_input=small_delivery,
                                                    inner_problem_solver=AStar(AirDistHeuristic, 0.5), roads=roads)
    run_astar_for_weights_in_range(MSTAirDistHeuristic, small_deliveries_prob)

    # Ex.28
    # TODO: create an instance of `AStar` with the `RelaxedDeliveriesHeuristic`,
    #       solve the `small_deliveries_strict_problem` with it and print the results (as before).
    small_deliveries_prob2 = StrictDeliveriesProblem(problem_input=small_delivery,
                                                     inner_problem_solver=AStar(AirDistHeuristic, 0.5), roads=roads)
    a_star = AStar(RelaxedDeliveriesHeuristic)
    res = a_star.solve_problem(small_deliveries_prob2)
    print(res)

def main():
    map_problem()
    relaxed_deliveries_problem()
    strict_deliveries_problem()


if __name__ == '__main__':
    main()
