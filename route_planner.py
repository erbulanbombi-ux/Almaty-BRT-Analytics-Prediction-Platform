from heapq import heappop, heappush


LRT_NETWORK = {
    "LRT-1": [("LRT-2", 3.2), ("LRT-3", 4.8)],
    "LRT-2": [("LRT-1", 3.2), ("LRT-3", 2.4), ("LRT-4", 3.6)],
    "LRT-3": [("LRT-1", 4.8), ("LRT-2", 2.4), ("LRT-4", 2.1), ("LRT-5", 4.2)],
    "LRT-4": [("LRT-2", 3.6), ("LRT-3", 2.1), ("LRT-5", 2.8)],
    "LRT-5": [("LRT-3", 4.2), ("LRT-4", 2.8), ("LRT-6", 3.5)],
    "LRT-6": [("LRT-5", 3.5)],
}


def dijkstra(start: str, end: str) -> dict:
    if start not in LRT_NETWORK or end not in LRT_NETWORK:
        raise ValueError("Unknown station")

    distances = {station: float("inf") for station in LRT_NETWORK}
    previous = {}
    distances[start] = 0.0
    queue = [(0.0, start)]

    while queue:
        distance, station = heappop(queue)
        if distance > distances[station]:
            continue
        if station == end:
            break
        for neighbor, weight in LRT_NETWORK[station]:
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = station
                heappush(queue, (candidate, neighbor))

    if distances[end] == float("inf"):
        raise ValueError("No route between stations")

    path = []
    station = end
    while station != start:
        path.append(station)
        station = previous[station]
    path.append(start)
    path.reverse()
    return {"stations": path, "distance_km": round(distances[end], 1)}


def simulate(traffic: int, passenger_demand: int, frequency: int) -> dict:
    traffic_factor = traffic / 100
    demand_factor = passenger_demand / 100
    frequency_factor = (30 - frequency) / 20
    delay = max(0.2, 1.1 + traffic_factor * 3.4 + demand_factor * 2.1 + frequency_factor * 1.8)
    travel_time = 22.0 + traffic_factor * 5.0 + demand_factor * 3.0 + frequency_factor * 2.0
    return {
        "delay_minutes": round(delay, 2),
        "travel_time_minutes": round(travel_time, 2),
        "on_time_probability": round(max(0.05, 1 - delay / 12), 2),
    }
