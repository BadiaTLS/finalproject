from datetime import time

def _create_graph(session):
    graph = {}
    session_items = list(session.items())

    for i in range(len(session_items) - 1):
        t1, seats1 = session_items[i]
        t2, seats2 = session_items[i + 1]
        graph[t1.strftime('%H:%M')] = {t2.strftime('%H:%M'): seats1}
    
    # Add the last time slot with no outgoing edges
    last_time_slot = session_items[-1][0]
    graph[last_time_slot.strftime('%H:%M')] = {last_time_slot.strftime('%H:%M'): session_items[-1][1]}
    
    return graph

session = {
    time(11, 0): 10,
    time(11, 30): 11,
    time(12, 0): 12,
    time(12, 30): 10,
    time(13, 0): 4,
    time(13, 30): 0
}

graph = _create_graph(session)
print(graph)
