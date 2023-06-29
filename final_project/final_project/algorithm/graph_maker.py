from datetime import time

def _create_graph(session):
    session_items = list(session.items())
    graph = {
        t1: {t2: seats1 for t2, seats2 in session_items[i+1:i+2]}
        for i, (t1, seats1) in enumerate(session_items[:-1])
    }
    
    last_time_slot, last_seats = session_items[-1]
    graph[last_time_slot] = {last_time_slot: last_seats}

    return graph


session = {
    time(11, 0): 10,
    time(11, 30): 11,
    time(12, 0): 12,
    time(12, 30): 16,
    time(13, 0): 4,
    time(13, 30): 1
}

# graph = _create_graph(session)
# print(graph)


from datetime import time

def create_graph(session):
    graph = {}

    # Add start node to the graph
    start_node = "S"
    graph[start_node] = {str(session_time): 0 for session_time in session}

    # Add intermediate nodes and their connections
    for session_time in session:
        node_name = str(session_time)
        node_weight = session[session_time]
        graph[node_name] = {"M": node_weight}

    # Add end node to the graph
    end_node = "E"
    graph[end_node] = {}

    # Connect start node to the intermediate nodes
    for node in graph.keys():
        if node != start_node and node != end_node:
            graph[start_node][node] = 0

    # Connect intermediate nodes to the end node
    for node in graph.keys():
        if node != start_node and node != end_node:
            graph[node][end_node] = 0

    return graph

# Usage example
session = {
    time(11, 0): 11,
    time(12, 0): 11,
    time(13, 0): 1,
    time(14, 0): 5,
}

# graph = create_graph(session)
# print(graph["S"])
# print(graph["M"])
# print(graph["E"])


session = {
    time(11, 0): 11,
    time(12, 0): 11,
    time(13, 0): 1,
    time(14, 0): 5,
}

graph = {"S": {'11:00': 0, '12:00': 0, '13:00': 0, '14:00': 0}}

for start_time, duration in session.items():
    start_node = str(start_time)
    middle_node = "M"
    end_node = "E"
    
    if start_node not in graph:
        graph[start_node] = {}
    
    graph[start_node].update({middle_node: duration})
    
    if middle_node not in graph:
        graph[middle_node] = {}
    
    graph[middle_node].update({end_node: 1})

# print(graph)

def convert_session_to_graph(session, start_node_label='S', middle_node_label='M', end_node_label='E'):
    graph = {start_node_label: {}}

    for start_time, duration in session.items():
        start_node = str(start_time)

        if start_node not in graph[start_node_label]:
            graph[start_node_label][start_node] = {}

        graph[start_node_label][start_node].update({middle_node_label: duration})

        if middle_node_label not in graph:
            graph[middle_node_label] = {}

        graph[middle_node_label].update({end_node_label: 1})

    return graph


session = {
    time(11, 0): 11,
    time(12, 0): 11,
    time(13, 0): 1,
    time(14, 0): 5,
}

graph = convert_session_to_graph(session)  # Using default labels
print(graph["S"])
print(graph["M"])

