def heuristic_minimize_delta(Network_Graph, Energy_C, source, Destination, packet_rate, packet_Size, power_transmit, Eneregy_rec):
    nodes = list(Network_Graph.keys())  # List of nodes
    P = packet_rate*1e-6   # Packets per unit time
    S = packet_Size*1e-6   # Size of each packet
    Pt = power_transmit*1e-6   # Transmission power
    E_tx = lambda d: power_transmit  # Transmission energy (simplified as constant)
    E_rx = Eneregy_rec  # Reception energy

    # Precompute link costs
    link_costs = {}
    for i in nodes:
        for j in Network_Graph[i]:
            link_costs[(i, j)] = 1 / min(Energy_C[i], Energy_C[j])

            # Find a path using a greedy algorithm
    # Find a path using a greedy algorithm
    def find_greedy_path(start, end, max_delta):
        path = [start]
        current = start
        visited = set()

        while current != end:
            visited.add(current)
            neighbors = Network_Graph[current]
            # Select the neighbor with the lowest cost that hasn't been visited
            next_node = None
            min_cost = float('inf')
            #print(current)
            for neighbor, dist in neighbors.items():
                if neighbor not in visited and Energy_C[neighbor] > 0:
                    cost = link_costs[(current, neighbor)]
                    #print(cost)
                    # Ensure max_delta constraint is satisfied
                    energy_after = Energy_C[current] - P * S * E_tx(dist)
                    energy_diff = abs(energy_after - Energy_C[neighbor])
                    #print(energy_diff)
                    if cost < min_cost and energy_diff <= max_delta:
                        min_cost = cost
                        next_node = neighbor

            if next_node is None:
                return None  # No feasible path found
            path.append(next_node)
            current = next_node

        return path
    # Compute energy consumption along the path
    def update_energy_levels(path):
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            d = Network_Graph[u][v]
            Energy_C[u] -= P * S * E_tx(d)
            Energy_C[v] -= P * S * E_rx

    # Iteratively minimize Delta
    min_delta = 0
    max_delta = max(Energy_C.values())-min(Energy_C.values())  # Initial Delta
    best_path = None
    #print(max_delta)
    while min_delta <= max_delta:
        current_delta = (min_delta + max_delta) / 2
        #print(current_delta,max_delta,min_delta)
        temp_energy = Energy_C.copy()
        path = find_greedy_path(source, Destination, current_delta)

        if path is not None:
            # Feasible path found, try smaller Delta
            best_path = path
            max_delta = current_delta - 1e-6  # Narrow down search
            Energy_C = temp_energy  # Revert to initial energy levels
        else:
            # No feasible path, increase Delta
            min_delta = current_delta + 1e-6

    # Output the best path and corresponding Delta
    if best_path is not None:
        update_energy_levels(best_path)
        final_delta = max(Energy_C.values()) - min(Energy_C.values())
        print(f"Minimized Delta: {final_delta:.6f}")
        print("Final energy levels:", Energy_C)
        print(f"Path from {source} to {Destination}: {best_path}")
        return best_path
    else:
        print("No feasible path found for any Delta.  ",current_delta)
        return None


# Example usage
if __name__ == "__main__":
    Network_Graph = { 
        'A': {'B': 40},
        'B': {'C': 20, 'E': 10, 'A': 40},
        'C': {'D': 30, 'F': 20, 'B': 20},
        'D': {'G': 70, 'C': 30},
        'E': {'H': 30, 'F': 70, 'B': 10},
        'H': {'E': 30, 'G': 40},
        'F': {'G': 20, 'C': 20, 'E': 70},
        'G': {'H': 40, 'D': 70, 'F': 20},
    }    
    import random
    #En = {'A': random.randint(100,110), 'B': random.randint(100,110), 'C': random.randint(100,110), 'D': random.randint(100,110), 
    #     'E': random.randint(100,110), 'H': random.randint(100,110), 'F': random.randint(100,110), 'G': random.randint(100,110)}
    global En
    En={'A': 100, 'B': 100, 'C':100, 'D': 100, 'E': 100, 'H': 100, 'F': 100, 'G': 100}
    #En={'1': 9319.697000000024, '2': 8073.493999999937, '3': 7980.6559999999445, '4': 9141.995999999981, '5': 8340.001999999913, '6': 9627.837000000027, '7': 8213.546999999917, '8': 9168.393999999953, '9': 7891.009999999933, '10': 9337.28799999999, '11': 99998489.91800183, '12': 9627.837000000027, '13': 9253.281000000052, '14': 9270.08800000005, '15': 9375.732000000044, '16': 9375.732000000044, '17': 9322.910000000047, '18': 8422.535000000107, '19': 9174.048000000057, '20': 9995.190000000002, '21': 9426.15300000004, '22': 9531.797000000033, '23': 9313.306000000048, '24': 9392.539000000043, '25': 9313.306000000048, '26': 9313.306000000048, '27': 9174.048000000057, '28': 9142.83500000006, '29': 9995.190000000002, '30': 9174.048000000057, '31': 9318.108000000047, '32': 9995.190000000002, '33': 9318.108000000047, '34': 9392.539000000043, '35': 9318.108000000047, '36': 9392.539000000043, '37': 9423.75200000004, '38': 9174.048000000057, '39': 8943.552000000072, '40': 9313.306000000048, '41': 9123.62700000006, '42': 9174.048000000057, '43': 9995.190000000002, '44': 9313.306000000048, '45': 9392.539000000043, '46': 9426.15300000004, '47': 9392.539000000043, '48': 9392.539000000043, '49': 9392.539000000043, '50': 9392.539000000043, '51': 9313.306000000048, '52': 9392.539000000043, '53': 9313.306000000048, '54': 7990.355000000136, '55': 9313.306000000048, '56': 9392.539000000043, '57': 9313.306000000048, '58': 9392.539000000043, '59': 9313.306000000048, '60': 9392.539000000043, '61': 9995.190000000002, '62': 9608.629000000028, '63': 9313.306000000048, '64': 9392.539000000043, '65': 9313.306000000048, '66': 9392.539000000043, '67': 9392.539000000043, '68': 9392.539000000043, '69': 9313.306000000048, '70': 9995.190000000002, '71': 9392.539000000043, '72': 9392.539000000043, '73': 9392.539000000043, '74': 9392.539000000043, '75': 9375.732000000044, '76': 9755.090000000018, '77': 9392.539000000043, '78': 9392.539000000043, '79': 9608.629000000028, '80': 9392.539000000043, '81': 9392.539000000043, '82': 9313.306000000048, '83': 9995.190000000002, '84': 9392.539000000043, '85': 9392.539000000043, '86': 9608.629000000028, '87': 9392.539000000043, '88': 9392.539000000043, '89': 9375.732000000044, '90': 9392.539000000043, '91': 9995.190000000002, '92': 9995.190000000002, '93': 9608.629000000028, '94': 9375.732000000044, '95': 9375.732000000044, '96': 9995.190000000002, '97': 9608.629000000028, '98': 9995.190000000002, '99': 9995.190000000002, '100': 9995.190000000002}
    source = 'A'
    Destination = 'G'
    packet_rate = 2
    packet_Size = 200
    power_transmit = 0.2
    Eneregy_rec = 0.5
    print(En)
    path= heuristic_minimize_delta(Network_Graph, En, source, Destination, packet_rate, packet_Size, power_transmit, Eneregy_rec)
