"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Adarsh Shresth
Student ID:   131073927

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    return ("Dijkstra from S finds the cheapest individual path to each node, but cannot "
        "decide the order in which relic chambers should be visited — and the visit "
        "order determines the total fuel cost.\n\n"

        "What decision remains after all inter-location costs are known: "
        "We still must choose the permutation of the relic chambers that minimizes "
        "cumulative fuel from S through every relic to T; the cost table alone does "
        "not reveal it.\n\n"

        "Why this requires a search over orders: "
        "The total cost depends on which relic is visited next at every step, so no "
        "single computation suffices — we must search the space of all possible orderings."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    sources = set()
    sources.add(spawn)
    for r in relics:
        sources.add(r)
    return list(sources)


def run_dijkstra(graph, source):
    nodes = set(graph.keys())

    for u in graph:
        for v, cost in graph[u]:
            nodes.add(v)

    dist = {node: float('inf') for node in nodes}
    dist[source] = 0

    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > dist[current_node]:
            continue

        for neighbor, weight in graph.get(current_node, []):
            new_distance = current_distance + weight

            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    dist_table = {}
    sources = select_sources(spawn, relics, exit_node)

    for source in sources:
        dist_table[source] = run_dijkstra(graph, source)

    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    return (
        "For nodes already finalized: each finalized node holds its true shortest-path "
        "distance from the source and that value will never change.\n\n"
        "For nodes not yet finalized: the current distance estimate is the cheapest path "
        "found so far using only finalized nodes as intermediates, it may still improve.\n\n"
        "Initialization: only the source gets distance 0 which is trivially correct, "
        "all other nodes start at infinity since no paths have been discovered yet.\n\n"
        "Maintenance: the node u extracted from the heap has the smallest tentative "
        "distance among all non-finalized nodes. Any alternative path to u must pass "
        "through a non-finalized node with distance >= dist[u], and since all edge "
        "weights are nonnegative, no alternative can be cheaper, so finalizing u is correct.\n\n"
        "Termination: when the heap is empty every reachable node holds its true "
        "shortest-path distance and unreachable nodes retain infinity.\n\n"
        "Why this matters: if any precomputed distance is wrong the planner may choose "
        "an ordering that appears cheaper but costs more fuel, making it impossible to "
        "guarantee the returned route is truly optimal."
    )



# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    return (
        "Why greedy fails: greedy always moves to the cheapest immediately reachable "
        "relic next, committing to a locally cheap step without considering the global "
        "cost of the remaining legs.\n\n"
        "Counter-example: relics A, B, C with costs S->A=1, S->B=2, S->C=2, "
        "A->B=100, A->C=1, A->T=1, B->A=1, B->C=1, B->T=1, C->A=1, C->B=100, C->T=100.\n\n"
        "What greedy picks: S->A (1, cheapest) -> A->C (1) -> C->B (100) -> B->T (1) = total 103.\n\n"
        "What optimal picks: S->B (2) -> B->C (1) -> C->A (1) -> A->T (1) = total 5.\n\n"
        "Why greedy loses: picking A first because it is cheapest from S forces the "
        "expensive C->B=100 leg to collect B. Optimal pays slightly more upfront "
        "to visit B first, which unlocks cheap hops for the rest of the route.\n\n"
        "What the algorithm must explore: every possible order in which the relic "
        "chambers can be visited, because the optimal order cannot be determined "
        "greedily and depends on the combined cost of the entire sequence."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    best = [float('inf'), []]
    relics_remaining = set(relics)

    _explore(
        dist_table=dist_table,
        current_loc=spawn,
        relics_remaining=relics_remaining,
        relics_visited_order=[],
        cost_so_far=0.0,
        exit_node=exit_node,
        best=best,
    )

    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    
    # Base case: all relics collected, travel to exit
    if not relics_remaining:
        dist_to_exit = dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        total_cost = cost_so_far + dist_to_exit
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = list(relics_visited_order)
        return

    # Recursive case: try each remaining relic as the next stop
    for relic in list(relics_remaining):
        travel_cost = dist_table.get(current_loc, {}).get(relic, float('inf'))
        if travel_cost == float('inf'):
            continue

        relics_remaining.remove(relic)
        relics_visited_order.append(relic)

        _explore(
            dist_table=dist_table,
            current_loc=relic,
            relics_remaining=relics_remaining,
            relics_visited_order=relics_visited_order,
            cost_so_far=cost_so_far + travel_cost,
            exit_node=exit_node,
            best=best,
        )

        # Backtrack
        relics_visited_order.pop()
        relics_remaining.add(relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
