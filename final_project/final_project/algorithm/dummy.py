from datetime import datetime, time

def _dijkstra_max_seats(graph, start, end):
    # Create a dictionary to store the maximum number of seats available from the start node to each node
    distances = {node: float('-inf') for node in graph}
    distances[start] = float('inf')

    # Create a set to keep track of visited nodes
    visited = set()

    while True:
        # Find the unvisited node with the maximum number of seats available
        current_node = None
        current_distance = float('-inf')
        for node, distance in distances.items():
            if node not in visited and distance > current_distance:
                current_node = node
                current_distance = distance

        # If no unvisited node was found, we're done
        if current_node is None:
            break

        # Mark the current node as visited
        visited.add(current_node)

        # Update the distances of the neighboring nodes
        for neighbor, weight in graph[current_node].items():
            distance = min(current_distance, weight)
            if distance > distances[neighbor]:
                distances[neighbor] = distance


    return distances[end]

# def _create_graph(session):
#     graph = {}
#     for t1, seats1 in session.items():
#         graph[t1.strftime('%H:%M')] = {}
#         for t2, seats2 in session.items():
#             if t1 < t2:
#                 graph[t1.strftime('%H:%M')][t2.strftime('%H:%M')] = max(seats1, seats2)
#     return graph

def _create_graph(session):
    graph = {}
    session_items = list(session.items())
    for i in range(len(session_items)):
        t1, seats1 = session_items[i]
        graph[t1.strftime('%H:%M')] = {}
        for j in range(i+1, len(session_items)):
            t2, seats2 = session_items[j]
            graph[t1.strftime('%H:%M')][t2.strftime('%H:%M')] = max(seats1, seats2)
    return graph

def get_recommended_time(session, start, end):
    
    start = datetime.strptime(start, '%H:%M').time()
    end = datetime.strptime(end, '%H:%M').time()
    session_start, session_end  = list(session.keys())[0], list(session.keys())[-1]

    key_list = list(session.keys())
    val_list = list(session.values())

    if start not in key_list or end not in key_list:
        print(start, end, session_start, session_end)
        if start > session_end: 
            return "No Available time"
        if start < session_start: 
            start = session_start.strftime("%H:%M")
        if end > session_end:
            end = session_end.strftime("%H:%M")
        else:
            return "No Available time"
    
    graph = _create_graph(session)
    max_seats = _dijkstra_max_seats(graph, start, end)
    
    position = val_list.index(max_seats)
    recommended_time = key_list[position].strftime("%H:%M")

    print(f"The maximum number of seats available between {start} and {end} is {max_seats}, and the time is {recommended_time}")

    return recommended_time



# def get_recommended_time(session, start, end):
#     graph = _create_graph(session)
#     max_seats = _dijkstra_max_seats(graph, start, end)

#     # list out keys and values separately
#     key_list = list(session.keys())
#     val_list = list(session.values())

#     # print key with val max_seats
#     position = val_list.index(max_seats)
#     recommended_time = key_list[position].strftime("%H:%M")

#     # print(f"The maximum number of seats available between {start} and {end} is {max_seats}, and the time is {recommended_time}")

#     return recommended_time

if __name__=="__main__":
    breakfast_session = {
        time(7,0): 1,
        time(7,30): 3,
        time(8,0): 3,
        time(8,30): 4,
        time(9,0): 6,
        time(9,30): 5,
    }
    start = '1:00'
    end = '15:00'

    ## CHECK START AND END BEFORE PUT IN
    get_recommended_time(breakfast_session, start, end)
