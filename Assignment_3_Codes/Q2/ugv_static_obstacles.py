import heapq
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

# Grid size: 70x70 km (each cell = 1 km)
GRID_SIZE = 70

# Obstacle density levels
DENSITY = {
    'low':    0.10,   # 10% of cells are obstacles
    'medium': 0.25,   # 25%
    'high':   0.40    # 40%
}


def generate_grid(size, obstacle_density, start, goal):
    """Generate a grid with random static obstacles."""
    grid = np.zeros((size, size), dtype=int)
    num_obstacles = int(size * size * obstacle_density)

    placed = 0
    while placed < num_obstacles:
        r = random.randint(0, size - 1)
        c = random.randint(0, size - 1)
        if (r, c) != start and (r, c) != goal and grid[r][c] == 0:
            grid[r][c] = 1
            placed += 1

    return grid


def heuristic(a, b):
    """Manhattan distance heuristic for A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    """
    A* algorithm (optimal shortest path with heuristic).
    Returns (path, nodes_explored, time_taken)
    """
    size = grid.shape[0]
    # 8-directional movement (including diagonals)
    directions = [(-1,0),(1,0),(0,-1),(0,1),
                  (-1,-1),(-1,1),(1,-1),(1,1)]
    move_cost = {(dr,dc): (1.414 if abs(dr)+abs(dc)==2 else 1.0)
                 for dr,dc in directions}

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, [start]))
    visited = {}
    nodes_explored = 0
    t_start = time.time()

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current in visited:
            continue
        visited[current] = g
        nodes_explored += 1

        if current == goal:
            return path, nodes_explored, time.time() - t_start

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] == 0:
                neighbor = (nr, nc)
                new_g = g + move_cost[(dr, dc)]
                if neighbor not in visited:
                    h = heuristic(neighbor, goal)
                    heapq.heappush(open_set, (new_g + h, new_g, neighbor, path + [neighbor]))

    return None, nodes_explored, time.time() - t_start  # No path found


def path_length(path):
    """Calculate total path length considering diagonal moves."""
    length = 0
    for i in range(1, len(path)):
        dr = abs(path[i][0] - path[i-1][0])
        dc = abs(path[i][1] - path[i-1][1])
        length += 1.414 if dr + dc == 2 else 1.0
    return length


def visualize_grid(grid, path, start, goal, density_name, ax):
    """Visualize the grid with obstacles and path."""
    display = np.copy(grid).astype(float)

    # Mark path
    if path:
        for (r, c) in path:
            display[r][c] = 2

    # Mark start/goal
    display[start[0]][start[1]] = 3
    display[goal[0]][goal[1]] = 4

    # Color map: 0=free, 1=obstacle, 2=path, 3=start, 4=goal
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'cyan', 'green', 'red'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    ax.imshow(display, cmap=cmap, norm=norm, origin='upper')
    ax.set_title(f'Density: {density_name.upper()}\n'
                 f'Path len: {path_length(path):.1f} km | Steps: {len(path)}',
                 fontsize=9)
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')

    # Legend
    patches = [
        mpatches.Patch(color='green', label='Start'),
        mpatches.Patch(color='red',   label='Goal'),
        mpatches.Patch(color='cyan',  label='Path'),
        mpatches.Patch(color='black', label='Obstacle'),
        mpatches.Patch(color='white', label='Free'),
    ]
    ax.legend(handles=patches, loc='upper right', fontsize=6)


def measures_of_effectiveness(path, nodes_explored, time_taken, density_name):
    """Print MoE for each run."""
    print(f"\n  {'─'*45}")
    print(f"  Density Level   : {density_name.upper()}")
    print(f"  Path Found      : {'Yes' if path else 'No'}")
    if path:
        print(f"  Path Length     : {path_length(path):.2f} km")
        print(f"  Steps in Path   : {len(path)}")
    print(f"  Nodes Explored  : {nodes_explored}")
    print(f"  Time Taken      : {time_taken*1000:.2f} ms")


# ─── MAIN ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    random.seed(42)

    START = (5, 5)
    GOAL  = (64, 64)

    print("=" * 60)
    print("    UGV PATHFINDING - STATIC OBSTACLES (A* Algorithm)")
    print(f"    Grid: {GRID_SIZE}x{GRID_SIZE} km | Start: {START} | Goal: {GOAL}")
    print("=" * 60)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('UGV Pathfinding - Static Obstacles (A* Algorithm)',
                 fontsize=14, fontweight='bold')

    for ax, (density_name, density_val) in zip(axes, DENSITY.items()):
        grid = generate_grid(GRID_SIZE, density_val, START, GOAL)
        path, nodes_explored, time_taken = astar(grid, START, GOAL)

        measures_of_effectiveness(path, nodes_explored, time_taken, density_name)

        if path:
            visualize_grid(grid, path, START, GOAL, density_name, ax)
        else:
            ax.text(0.5, 0.5, 'No Path Found', transform=ax.transAxes,
                    ha='center', va='center', fontsize=14, color='red')
            ax.set_title(f'Density: {density_name.upper()} - NO PATH')

    plt.tight_layout()
    plt.savefig('ugv_static_obstacles.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\nVisualization saved as 'ugv_static_obstacles.png'")
