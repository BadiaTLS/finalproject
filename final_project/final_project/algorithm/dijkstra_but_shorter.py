from datetime import time
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

def convert_session_to_graph(session, start_node_label='S', middle_node_label='M', end_node_label='E'):
    graph = {start_node_label: {}}

    for start_time, duration in session.items():
        start_node = str(start_time)

        if start_node not in graph[start_node_label]:
            graph[start_node_label][start_node] = 0

        graph[start_node] = {middle_node_label: duration}
        # graph[start_node_label][start_node].update({middle_node_label: duration})
        print(duration)

        if middle_node_label not in graph:
            graph[middle_node_label] = {}

        graph[middle_node_label].update({end_node_label: 1})
        graph[end_node_label] = {}

    return graph

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

graph = {'S': {'11:00:00': 0, '11:30:00': 0, '12:00:00': 0, '12:30:00': 0, '13:00:00': 0, '13:30:00': 0, '14:00:00': 0}, 
         '11:00:00': {'M': 10}, 
         'M': {'E': 1}, 
         'E': {}, 
         '11:30:00': {'M': 11}, 
         '12:00:00': {'M': 12}, 
         '12:30:00': {'M': 16}, 
         '13:00:00': {'M': 4}, 
         '13:30:00': {'M': 1}, 
         '14:00:00': {'M': 0}}

# Example session schedule
session = {
    time(11, 0): 10,
    time(11, 30): 11,
    time(12, 0): 12,
    time(12, 30): 16,
    time(13, 0): 4,
    time(13, 30): 0,
    time(14, 0): 1,
}

# Example usage
graph = convert_session_to_graph(session)
print(graph)

shortest_distance, shortest_path, path_times = dijkstra(graph, "S", "E")
print("Shortest distance from S to E:", shortest_distance)
print("Shortest path from S to E:", shortest_path)
print("Corresponding times for each step:", path_times)

import heapq

