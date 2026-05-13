# Development Log – The Torchbearer

**Student Name:** Adarsh Shresth
**Student ID:** 131073927

---

## Entry 1 – 5/10: Initial Plan

Before writing any code, I mapped out the two-phase structure: first precompute all 
necessary shortest-path distances using Dijkstra, then search over orderings of the 
relic set. I expect the Dijkstra implementation to be straightforward since we covered 
it in lecture, but the search phase with correct backtracking and pruning will need 
careful thought. I plan to implement and test Dijkstra first, then layer the recursive 
search on top, adding pruning once the brute-force version passes the provided tests.

---

## Entry 2 – 5/11 : Implemented Parts 1-2

My initial assumption was that the exit node should be included as a Dijkstra source, 
but after thinking through the lookup pattern I realized exit is always a destination 
and never a starting point, so it doesn't need its own run. Also had to think carefully 
about nodes that appear only as neighbors and never as graph keys - solved it by 
collecting all nodes upfront before initializing the dist table. Filled in README Parts 1 and 2.

---

## Entry 3 – 5/12 : Search implementation and written sections

Implemented dijkstra_invariant_check, explain_search, find_optimal_route, _explore, 
and solve. All four provided tests pass with the brute-force backtracking approach. 
The trickiest part was getting backtracking right, removing a relic from 
relics_remaining before recursing and adding it back after. Also filled in README 
Parts 3, 4, and 5.
---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
