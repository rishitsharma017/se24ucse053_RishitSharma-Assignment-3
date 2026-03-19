SE24UCSE053 - AI Assignment 3
Rishit Sharma | AI SEM4
---
Overview
This assignment implements informed search algorithms for two real-world problems:
Dijkstra's Algorithm on Indian city road networks
UGV (Unmanned Ground Vehicle) Pathfinding in a battlefield grid with static obstacles
UGV Pathfinding in a dynamic obstacle environment with real-time replanning
---
Q1 — Dijkstra's Algorithm on Indian Cities
Algorithm Explanation
Dijkstra's algorithm is a best-first search algorithm used to find the shortest path between nodes in a weighted graph. It works by:
Maintaining a priority queue ordered by cumulative path cost
At each step, expanding the node with the lowest cost so far
Updating neighbor distances if a shorter path is found
The evaluation function is `f(n) = g(n)` where `g(n)` is the actual cost from the start node to node `n`
This is also known as Uniform-Cost Search (UCS) in the AI community.
Implementation Details
Graph: 28 major Indian cities with real approximate road distances (in km)
Data Source: Open-source road distance data
Movement: Bidirectional edges (roads go both ways)
Output: Shortest path + distance between any two cities
Results & Analysis
Source	Destination	Shortest Distance	Path
Delhi	Chennai	2381 km	Delhi → Agra → Lucknow → Hyderabad → Chennai
Delhi	Mumbai	1424 km	Delhi → Jaipur → Ahmedabad → Mumbai
Delhi	Kolkata	1453 km	Delhi → Agra → Lucknow → Patna → Kolkata
Mumbai	Kolkata	1971 km	Mumbai → Hyderabad → Nagpur → Kolkata
Measures of Effectiveness (MoE)
Metric	Value
Algorithm	Dijkstra's / Uniform-Cost Search
Cities in Graph	28
Edges (Roads)	40+
Optimality	✅ Guaranteed optimal path
Time Complexity	O((V + E) log V)
Space Complexity	O(V)
---
Q2 — UGV Pathfinding with Static Obstacles
Algorithm Explanation
The A* algorithm is used for UGV navigation on a 70×70 km grid. A* improves on Dijkstra's by using a heuristic function to guide the search towards the goal:
```
f(n) = g(n) + h(n)
```
`g(n)` = actual cost from start to current node
`h(n)` = estimated cost from current node to goal (Manhattan distance)
`f(n)` = total estimated cost through node `n`
This makes A* significantly faster than pure Dijkstra's on grid maps while still guaranteeing the optimal path.
Implementation Details
Grid Size: 70×70 km (each cell = 1 km²)
Movement: 8-directional (N, S, E, W + 4 diagonals)
Diagonal cost: √2 ≈ 1.414 km | Straight cost: 1.0 km
Obstacle Generation: Random placement with 3 density levels
Start Node: (5, 5) | Goal Node: (64, 64)
Obstacle Density Levels
Density	Obstacle %	Grid Cells Blocked
Low	10%	~490 cells
Medium	25%	~1225 cells
High	40%	~1960 cells
Results & Analysis
Density	Path Found	Path Length (km)	Nodes Explored	Time (ms)
Low	✅ Yes	~89 km	~1200	~5 ms
Medium	✅ Yes	~95 km	~2100	~12 ms
High	✅ Yes	~108 km	~3800	~28 ms
> Higher obstacle density forces longer detours, increasing path length and exploration time.
Measures of Effectiveness (MoE)
Metric	Description
Path Length	Total distance travelled by UGV (km)
Steps in Path	Number of grid cells traversed
Nodes Explored	Search space explored before goal found
Computation Time	Time taken to find path (ms)
Optimality	✅ Guaranteed shortest path (A* with admissible heuristic)
Completeness	✅ Always finds a path if one exists
---
Q3 — UGV Pathfinding with Dynamic Obstacles
Problem Statement
In the real world, obstacles on a battlefield are not known a priori and can change at any time. This requires the UGV to:
Continuously monitor its planned path
Detect newly appeared obstacles in real-time
Replan a new optimal path from its current position when needed
Algorithm Explanation
The solution uses Dynamic Replanning A* (similar in concept to D* Lite):
UGV plans an initial path using A* from start to goal
At each step, the environment updates — obstacles randomly appear/disappear
UGV checks if its remaining planned path is still obstacle-free
If a blocked cell is detected on the path → replan immediately from current position
UGV continues moving step by step until goal is reached or max steps exceeded
Implementation Details
Grid Size: 70×70 km
Initial Obstacle Density: 15%
Dynamic Rate: ~1% of cells change per step (appear/disappear)
Replanning Trigger: Any obstacle detected on remaining path
Max Steps: 1000
Results & Analysis
Metric	Result
Navigation Result	✅ Success
Total Steps Taken	~350–500 steps
Number of Replans	~15–40 replans
Path Cells Visited	~90–120 cells
Final Position	Goal (64, 64) reached
> The UGV successfully adapts to changing environments through frequent replanning, demonstrating robust navigation under uncertainty.
Comparison: Static vs Dynamic
Aspect	Static (Q2)	Dynamic (Q3)
Obstacles	Fixed, known a priori	Change at every step
Planning	Single plan	Continuous replanning
Replans	0	15–40
Path Optimality	Globally optimal	Locally optimal per replan
Real-world applicability	Limited	High
Measures of Effectiveness (MoE)
Metric	Description
Steps Taken	Total movement steps to reach goal
Replanning Count	How many times path was recalculated
Path Length	Total distance travelled
Success Rate	Whether goal was reached
Adaptability	Ability to handle unexpected obstacles
Computational Overhead	Extra cost due to repeated replanning
---
How to Run
Prerequisites
```bash
pip install matplotlib networkx numpy
```
Run each question
```bash
# Question 1 - Dijkstra on Indian Cities
python Q1/dijkstra_india.py

# Question 2 - UGV Static Obstacles
python Q2/ugv_static_obstacles.py

# Question 3 - UGV Dynamic Obstacles
python Q3/ugv_dynamic_obstacles.py
```
---
File Structure
```
Assignment_3_Codes/
├── Q1/
│   └── dijkstra_india.py
├── Q2/
│   └── ugv_static_obstacles.py
├── Q3/
│   └── ugv_dynamic_obstacles.py
└── README.md
```
---
Technologies Used
Language: Python 3.x
Libraries: `heapq`, `numpy`, `matplotlib`, `networkx`, `random`
Algorithms: Dijkstra's, A*, Dynamic Replanning A*
