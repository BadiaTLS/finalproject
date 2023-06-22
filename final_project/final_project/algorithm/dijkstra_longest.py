import heapq

def dijkstra(graph, start='S', end='E'):
    distances = {node: float('-inf') for node in graph}
    distances[start] = 0
    priority_queue = [(distances[start], start)]  # Use positive distance for min-heap
    visited = set()
    previous = {}
    time = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            new_distance = current_distance + weight  # Use addition for longest distance
            if new_distance > distances[neighbor]:  # Compare with longest distance
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                time[neighbor] = weight
                heapq.heappush(priority_queue, (new_distance, neighbor))

    longest_distance = distances[end]
    longest_path = [end]
    current_node = end

    while current_node != start:
        current_node = previous[current_node]
        longest_path.append(current_node)

    longest_path = longest_path[::-1]
    path_times = [time[node] for node in longest_path[1:]]

    return longest_distance, longest_path, path_times

def convert_session_to_graph(session, start_node_label='S', middle_node_label='M', end_node_label='E'):
    graph = {start_node_label: {}}

    for start_time, duration in session.items():
        start_node = str(start_time)

        if start_node not in graph[start_node_label]:
            graph[start_node_label][start_node] = 0

        graph[start_node] = {middle_node_label: duration}
        # graph[start_node_label][start_node].update({middle_node_label: duration})
        if middle_node_label not in graph:
            graph[middle_node_label] = {}

        graph[middle_node_label].update({end_node_label: 1})
        graph[end_node_label] = {}

    return graph

def update_session_by_start_end(session, start, end):
    # Here to check session
    return session

def get_recommended_time(session, start_time, end_time):
    session = update_session_by_start_end(session=session, start = start_time, end= end_time)

    graph = convert_session_to_graph(session)
    longest_distance, longest_path, path_times = dijkstra(graph=graph)

    print("Longest Distance:", longest_distance)
    print("Longest Path:", longest_path)
    print("Path Times:", path_times)
    recommended_time = longest_path[1]
    return recommended_time

if __name__ == "__main__":
    from datetime import time
    # Example usage:
    session = {
        time(11, 0): 100,
        time(11, 30): 11,
        time(12, 0): 12,
        time(12, 30): 10,
        time(13, 0): 4,
        time(13, 30): 0,
        time(13, 0): 0,
    }
    start_time = '?'
    end_time = '?'

    result = get_recommended_time(session=session, start_time=start_time, end_time=end_time)
    print(result)
