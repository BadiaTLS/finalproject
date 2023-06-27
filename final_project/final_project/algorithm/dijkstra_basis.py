import heapq

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    visited = set()
    previous = {}
    time = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        visited.add(current_node)

        if current_node == end:
            break

        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    time[neighbor] = weight
                    heapq.heappush(priority_queue, (new_distance, neighbor))

    shortest_distance = distances[end]
    shortest_path = [end]
    current_node = end

    while current_node != start:
        current_node = previous[current_node]
        shortest_path.append(current_node)

    shortest_path = shortest_path[::-1]
    path_times = [time[node] for node in shortest_path[1:]]

    return shortest_distance, shortest_path, path_times

# Usage
graph = {
    "S": {'11:00': 0, '12:00': 0, '13:00': 0, '14:00': 0},
    '11:00': {"M": 11},
    '12:00': {'M': 11},
    '13:00': {'M': 1},
    '14:00': {'M': 5},
    "M": {"E": 0},
    "E": {},
}

shortest_distance, shortest_path, path_times = dijkstra(graph, "S", "E")
print("Shortest distance from S to E:", shortest_distance)
print("Shortest path from S to E:", shortest_path)
print("Corresponding times for each step:", path_times)
