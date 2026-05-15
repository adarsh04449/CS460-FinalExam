# The Torchbearer

**Student Name:** Adarsh Shresth
**Student ID:** 131073927
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single Dijkstra run from S gives the minimum cost to reach each node individually, but cannot determine the best order to visit the relic chambers.


- **What decision remains after all inter-location costs are known:**
  We still must choose the order in which to visit all relic chambers before reaching the exit T.

- **Why this requires a search over orders (one sentence):**
  Different visitation orders of the relics lead to different total costs, so we must search over all possible orderings to find the minimum.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Entrance node (spawn) | The Torchbearer starts here, so we need cheapest costs from spawn to every relic and to T. |
| Each relic chamber | After collecting a relic the Torchbearer departs from it, so we need costs outward from every relic to the next destination. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary: `dist_table[source][destination]` |
| What the keys represent | Source nodes — spawn and each relic chamber |
| What the values represent | Inner dict mapping every reachable node to its minimum fuel cost from that source |
| Lookup time complexity | O(1) average |
| Why O(1) lookup is possible | Python dicts use hash tables; both the outer and inner key lookups resolve in constant time. |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** `k + 1, where k = |M|`
- **Cost per run:** `O(m log n), where m = |E| and n = |V|`
- **Total complexity:** `O((k + 1) · m log n) = O(k · m log n)` 
- **Justification:** Dijkstra runs once from the spawn node and once from each of the `k` relics.

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  Every finalized node holds its true minimum-cost distance from the source; this value is permanent and will never be updated again

- **For nodes not yet finalized (not in S):**
  The current distance estimate is the cheapest path found so far that only uses finalized nodes as intermediates; it is an upper bound that may still decrease

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  Only the source gets distance 0, which is trivially correct. All other nodes start at infinity since no paths have been discovered yet, so the invariant holds before the first iteration

- **Maintenance : why finalizing the min-dist node is always correct:**
  The node extracted from the heap always has the smallest tentative distance among all non-finalized nodes. Any alternative path to it must pass through a non-finalized node whose distance is already >= the extracted node's distance, and since all edge weights are nonnegative, extending that path cannot make it cheaper. So finalizing it is always correct

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the heap is empty every reachable node is finalized and holds its true shortest-path distance; unreachable nodes correctly retain infinity

### Part 3c: Why This Matters for the Route Planner
  If any precomputed distance is incorrect the planner may select a relic ordering that appears cheaper but actually costs more fuel, making it impossible to guarantee the returned route is truly optimal

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Greedy commits to the nearest unvisited relic at every step without considering how that choice affects the cost of all remaining legs
- **Counter-example setup:** S->A=1, S->B=2, S->C=2, A->B=100, A->C=1, A->T=1, B->A=1, B->C=1, B->T=1, C->A=1, C->B=100, C->T=100
- **What greedy picks:** S->A (1, nearest) -> A->C (1) -> C->B (100) -> B->T (1) = total 103
- **What optimal picks:** S->B (2) -> B->C (1) -> C->A (1) -> A->T (1) = total 5
- **Why greedy loses:** Picking A first because it is the cheapest next hop forces the expensive C->B=100 leg to collect B, while optimal pays slightly more upfront to visit B first and unlocks cheap hops for the rest of the route

### What the Algorithm Must Explore

- The algorithm must explore every possible order in which the relic chambers can be visited, because the optimal order cannot be determined greedily and depends on the combined cost of the entire sequence from S through all relics to T

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | `current_loc` | node (str or int) | The node where the Torchbearer currently stands |
| Relics already collected | `relics_visited_order` | list[node] | Ordered sequence of relics collected so far |
| Fuel cost so far | `cost_so_far` | float | Cumulative torch fuel spent to reach this state |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | Python `set` (`relics_remaining`) |
| Operation: check if relic already collected | O(1) average - hash lookup |
| Operation: mark a relic as collected | O(1) average - `set.remove` |
| Operation: unmark a relic (backtrack) | O(1) average - `set.add` |
| Why this structure fits | Constant-time membership check and add/remove keeps each level of the recursive search efficient and backtracking is a single O(1) operation. |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k! 
- **Why:** In the worst case there is no pruning and the algorithm explores every permutation of the k relic chambers, and the number of permutations of k items is k factorial

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking


- **What is tracked:** A mutable list `best` holding the lowest complete-route fuel cost seen so far in `best[0]` and the relic ordering that achieved it in `best[1]`
- **When it is used:** At the start of every recursive call, the current lower-bound estimate is compared against `best[0]` to decide whether to continue or prune
- **What it allows the algorithm to skip:** Any branch whose lower-bound cost already meets or exceeds `best[0]` is abandoned, avoiding exploration of all sub-orderings beneath it

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** We know `cost_so_far`, the current location, and the precomputed shortest distance from the current location to the exit node
- **What the lower bound accounts for:** It adds `cost_so_far` and the minimum possible cost to reach the exit, treating all remaining unvisited relics as if they could be collected for free
- **Why it never overestimates:** Collecting remaining relics always costs nonnegative fuel on top of the exit leg, so the bound is always less than or equal to the true remaining cost

### Part 6c: Pruning Correctness

- If `cost_so_far + dist_to_exit >= best[0]`, every possible completion of this branch costs at least that much, which cannot improve on `best[0]`. The optimal solution is either already recorded in `best` or lives in a branch that has not been pruned.
- The bound never overestimates the true cost, so any branch that could contain the optimal solution will have a lower bound strictly below `best[0]` and will not be pruned.

---

## References

- Lecture notes only.