"""
examples.py
===========
Complete runnable examples demonstrating all graph types and features.

Run any example:
    python examples.py directed_city_network
    python examples.py undirected_social
    python examples.py multi_edge_airline
    ... etc
"""

from graph import Graph
from graph_renderer import render_graph


# ══════════════════════════════════════════════════════════════════════════════
#  Example 1: Directed Graph — City Network
# ══════════════════════════════════════════════════════════════════════════════

def example_directed_city_network():
    """
    A directed weighted graph of German cities and distances.
    Demonstrates: basic directed graph, weights, traversal.
    """
    print("=" * 70)
    print("EXAMPLE 1: Directed Graph — City Network")
    print("=" * 70)
    print()

    g = Graph(directed=True, name="GermanCities")

    # Add cities with population data
    cities = {
        "Berlin": 3_700_000,
        "Munich": 1_500_000,
        "Hamburg": 1_800_000,
        "Cologne": 1_100_000,
        "Frankfurt": 750_000,
    }

    for city, population in cities.items():
        g.add_node(city, data={"population": population})

    # Add routes (distance in km)
    routes = [
        ("Berlin", "Munich", 585),
        ("Berlin", "Hamburg", 289),
        ("Hamburg", "Cologne", 390),
        ("Cologne", "Frankfurt", 180),
        ("Frankfurt", "Munich", 365),
        ("Munich", "Frankfurt", 365),
    ]

    for src, dst, distance in routes:
        g.add_edge(src, dst, weight=distance)

    # Display
    print(render_graph(g, format="ascii"))
    print()

    # Queries
    print("Network Analysis:")
    print(f"  Total cities: {g.order()}")
    print(f"  Total routes: {g.size()}")
    print()

    print("Outgoing routes from Berlin:")
    for neighbor in g.neighbors("Berlin"):
        edges = g.get_edges("Berlin", neighbor.node_id)
        for edge in edges:
            print(f"  → {neighbor.node_id} ({edge.weight} km)")
    print()

    print("Cities that can reach Hamburg:")
    in_edges = g.in_edges("Hamburg")
    if in_edges:
        for edge in in_edges:
            print(f"  ← {edge.src.node_id} ({edge.weight} km)")
    else:
        print("  (None)")
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  Example 2: Undirected Graph — Social Network
# ══════════════════════════════════════════════════════════════════════════════

def example_undirected_social_network():
    """
    An undirected graph of friends (symmetric relationships).
    Demonstrates: undirected edges, symmetric neighbors, degree.
    """
    print("=" * 70)
    print("EXAMPLE 2: Undirected Graph — Social Network")
    print("=" * 70)
    print()

    g = Graph(directed=False, name="FriendNetwork")

    # Add friends
    friendships = [
        ("Alice", "Bob"),
        ("Bob", "Charlie"),
        ("Alice", "Charlie"),
        ("Charlie", "David"),
        ("David", "Eve"),
        ("Eve", "Alice"),
        ("Alice", "Frank"),
    ]

    for person_a, person_b in friendships:
        g.add_edge(person_a, person_b)

    # Display
    print(render_graph(g, format="ascii"))
    print()

    # Queries
    print("Network Statistics:")
    print(f"  Total people: {g.order()}")
    print(f"  Total friendships: {g.size()}")
    print()

    print("Friend count per person:")
    for person in sorted([n.node_id for n in g.nodes()]):
        friend_count = g.degree(person)
        friends = [n.node_id for n in g.neighbors(person)]
        print(f"  {person}: {friend_count} friends {friends}")
    print()

    # Find most connected person
    most_connected = max(g.nodes(), key=lambda n: g.degree(n.node_id))
    print(f"Most connected person: {most_connected.node_id} ({g.degree(most_connected.node_id)} friends)")
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  Example 3: Weighted Directed Graph
# ══════════════════════════════════════════════════════════════════════════════

def example_weighted_directed():
    """
    Weighted directed graph: network costs/delays.
    Demonstrates: weights for numeric meaning, out_degree, in_degree.
    """
    print("=" * 70)
    print("EXAMPLE 3: Weighted Directed Graph — Network Delays")
    print("=" * 70)
    print()

    g = Graph(directed=True, name="NetworkLatency")

    servers = ["ServerA", "ServerB", "ServerC", "ServerD"]
    for server in servers:
        g.add_node(server, data={"status": "online"})

    # Add communication links (latency in ms)
    links = [
        ("ServerA", "ServerB", 5.2),
        ("ServerA", "ServerC", 12.1),
        ("ServerB", "ServerC", 3.8),
        ("ServerB", "ServerD", 8.5),
        ("ServerC", "ServerD", 2.1),
    ]

    for src, dst, latency in links:
        g.add_edge(src, dst, weight=latency)

    print(render_graph(g, format="ascii"))
    print()

    # Analysis
    print("Latency Analysis:")
    for server in servers:
        out_deg = g.out_degree(server)
        in_deg = g.in_degree(server)
        print(f"  {server}: sends to {out_deg} servers, receives from {in_deg} servers")
    print()

    # Total outgoing latency from ServerA
    total_out_latency = sum(e.weight for e in g.out_edges("ServerA"))
    print(f"Total latency from ServerA: {total_out_latency:.1f} ms")
    print()

    # Lowest latency link
    all_edges = list(g.edges())
    lowest = min(all_edges, key=lambda e: e.weight)
    print(f"Lowest latency link: {lowest.src.node_id} → {lowest.dst.node_id} ({lowest.weight} ms)")
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  Example 4: Multi-Edge Graph
# ══════════════════════════════════════════════════════════════════════════════

def example_multi_edge_airline():
    """
    Multi-edge graph: multiple flights on the same route.
    Demonstrates: parallel edges, edge attributes, get_edges().
    """
    print("=" * 70)
    print("EXAMPLE 4: Multi-Edge Graph — Airline Network")
    print("=" * 70)
    print()

    g = Graph(directed=True, name="Airlines")

    airports = ["JFK", "LAX", "ORD", "ATL", "DEN"]
    for airport in airports:
        g.add_node(airport, data={"type": "airport"})

    # Multiple flights per route
    flights = [
        ("JFK", "LAX", 5.5, "United", "Boeing 777"),
        ("JFK", "LAX", 5.5, "American", "Airbus A350"),
        ("JFK", "ORD", 2.5, "Delta", "Boeing 737"),
        ("LAX", "DEN", 2.0, "Southwest", "Boeing 737"),
        ("ORD", "ATL", 2.0, "United", "Boeing 787"),
    ]

    for src, dst, hours, airline, aircraft in flights:
        g.add_edge(src, dst, weight=hours, airline=airline, aircraft=aircraft)

    print(render_graph(g, format="ascii"))
    print()

    # Find all flights on a route
    print("Flight Options:")
    routes = [("JFK", "LAX"), ("JFK", "ORD"), ("LAX", "DEN")]
    for src, dst in routes:
        flights_on_route = g.get_edges(src, dst)
        print(f"  {src} → {dst}: {len(flights_on_route)} flight(s)")
        for flight in flights_on_route:
            airline = flight.get_attr("airline")
            aircraft = flight.get_attr("aircraft")
            hours = flight.weight
            print(f"    • {airline:12} {aircraft:20} ({hours}h)")
    print()

    # Airport statistics
    print("Airport Statistics:")
    for airport in airports:
        outgoing = g.out_degree(airport)
        incoming = g.in_degree(airport)
        print(f"  {airport}: {outgoing} outgoing, {incoming} incoming")
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  Example 5: Self-Loop Graph
# ══════════════════════════════════════════════════════════════════════════════

def example_self_loop_state_machine():
    """
    Directed graph with self-loops: state machine.
    Demonstrates: self-loops, state transitions, cycle detection.
    """
    print("=" * 70)
    print("EXAMPLE 5: Self-Loop Graph — Process State Machine")
    print("=" * 70)
    print()

    g = Graph(directed=True, name="ProcessStateMachine")

    states = ["Idle", "Running", "Paused", "Error", "Shutdown"]
    for state in states:
        g.add_node(state, data={"type": "state"})

    # Transitions (including self-loops for retries)
    transitions = [
        ("Idle", "Running", 1.0),
        ("Running", "Paused", 1.0),
        ("Paused", "Running", 1.0),
        ("Running", "Error", 1.0),
        ("Error", "Idle", 1.0),
        ("Error", "Error", 0.5),  # Self-loop: retry with 50% weight
        ("Running", "Shutdown", 1.0),
    ]

    for src, dst, weight in transitions:
        g.add_edge(src, dst, weight=weight)

    print(render_graph(g, format="ascii"))
    print()

    # Analysis
    print("State Transition Analysis:")
    for state in states:
        out_deg = g.out_degree(state)
        self_loops = g.get_edges(state, state)
        neighbors = g.neighbors(state)
        print(f"  {state}:")
        print(f"    Outgoing transitions: {out_deg}")
        print(f"    Self-loops: {len(self_loops)}")
        next_states = [n.node_id for n in neighbors if n.node_id != state]
        if next_states:
            print(f"    Can transition to: {next_states}")
        print()

    # Find states with self-loops
    print("States with retry capability (self-loops):")
    for state in states:
        self_loops = g.get_edges(state, state)
        if self_loops:
            print(f"  {state} (retry weight: {self_loops[0].weight})")
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  Example 6: Copy and Subgraph
# ══════════════════════════════════════════════════════════════════════════════

def example_copy_and_subgraph():
    """
    Graph operations: copy and subgraph extraction.
    Demonstrates: g.copy(), g.subgraph(), graph independence.
    """
    print("=" * 70)
    print("EXAMPLE 6: Graph Operations — Copy and Subgraph")
    print("=" * 70)
    print()

    # Create original graph
    g = Graph(directed=True, name="Original")

    nodes = ["A", "B", "C", "D", "E"]
    for node in nodes:
        g.add_node(node)

    edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("A", "E")]
    for src, dst in edges:
        g.add_edge(src, dst)

    print("Original Graph:")
    print(render_graph(g, format="ascii"))
    print()

    # Full copy
    g_copy = g.copy()
    g_copy.add_node("Z")
    print("After adding 'Z' to copy:")
    print(f"  Original nodes: {g.order()}")
    print(f"  Copy nodes: {g_copy.order()}")
    print(f"  Independent? Yes (original unaffected)")
    print()

    # Subgraph
    sub = g.subgraph(["A", "B", "C"])
    print("Subgraph of ['A', 'B', 'C']:")
    print(render_graph(sub, format="ascii"))
    print()

    print("Subgraph analysis:")
    print(f"  Nodes: {sub.order()}")
    print(f"  Edges: {sub.size()}")
    print(f"  A → B exists? {sub.has_edge('A', 'B')}")
    print(f"  A → E exists? {sub.has_edge('A', 'E')}")  # False (E not in subgraph)
    print(f"  D in subgraph? {sub.has_node('D')}")  # False
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  Example 7: Complex Real-World Example — E-Commerce System
# ══════════════════════════════════════════════════════════════════════════════

def example_ecommerce_system():
    """
    Complex example: e-commerce order workflow with multiple edge types.
    Demonstrates: rich attributes, data payloads, realistic graph design.
    """
    print("=" * 70)
    print("EXAMPLE 7: Complex Example — E-Commerce Order Workflow")
    print("=" * 70)
    print()

    g = Graph(directed=True, name="OrderWorkflow")

    # Workflow stages
    stages = {
        "Pending": "Awaiting payment",
        "Processing": "Order being prepared",
        "Shipped": "In transit",
        "Delivered": "Customer received",
        "Cancelled": "Order cancelled",
        "Returned": "Product returned",
    }

    for stage, description in stages.items():
        g.add_node(stage, data={"description": description})

    # Transitions with metadata
    transitions = [
        ("Pending", "Processing", {"action": "payment_confirmed", "time_est": 0.5}),
        ("Pending", "Cancelled", {"action": "customer_cancellation", "time_est": 0.0}),
        ("Processing", "Shipped", {"action": "fulfillment_complete", "time_est": 2.0}),
        ("Processing", "Cancelled", {"action": "inventory_unavailable", "time_est": 0.0}),
        ("Shipped", "Delivered", {"action": "delivery_complete", "time_est": 5.0}),
        ("Shipped", "Returned", {"action": "return_initiated", "time_est": 3.0}),
        ("Delivered", "Returned", {"action": "customer_return", "time_est": 7.0}),
        ("Cancelled", "Pending", {"action": "customer_reorder", "time_est": 0.0}),
        ("Returned", "Pending", {"action": "restock", "time_est": 0.0}),
    ]

    for src, dst, metadata in transitions:
        action = metadata["action"]
        time = metadata["time_est"]
        g.add_edge(src, dst, weight=time, action=action)

    print(render_graph(g, format="ascii"))
    print()

    # Analysis
    print("Workflow Analysis:")
    print(f"  Total stages: {g.order()}")
    print(f"  Total transitions: {g.size()}")
    print()

    print("Order path possibilities:")
    start = "Pending"
    print(f"  From {start}:")
    for neighbor in g.neighbors(start):
        next_state = neighbor.node_id
        edges = g.get_edges(start, next_state)
        for edge in edges:
            action = edge.get_attr("action")
            time = edge.weight
            print(f"    → {next_state:12} (action: {action:25} ~{time}d)")
    print()

    print("Delivery path (typical happy path):")
    path = ["Pending", "Processing", "Shipped", "Delivered"]
    for i, state in enumerate(path):
        if i < len(path) - 1:
            next_state = path[i + 1]
            edges = g.get_edges(state, next_state)
            if edges:
                time = edges[0].weight
                print(f"  {state:12} → {next_state:12} (~{time}d)")
        else:
            print(f"  {state:12} ✓ Complete")
    print()

    # Return path
    print("Return path:")
    return_path = ["Delivered", "Returned", "Pending"]
    for i, state in enumerate(return_path):
        if i < len(return_path) - 1:
            next_state = return_path[i + 1]
            edges = g.get_edges(state, next_state)
            if edges:
                time = edges[0].weight
                print(f"  {state:12} → {next_state:12} (~{time}d)")
        else:
            print(f"  {state:12} (ready for reorder)")
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  Main runner
# ══════════════════════════════════════════════════════════════════════════════

EXAMPLES = {
    "directed_city_network": example_directed_city_network,
    "undirected_social": example_undirected_social_network,
    "weighted_directed": example_weighted_directed,
    "multi_edge_airline": example_multi_edge_airline,
    "self_loop_state": example_self_loop_state_machine,
    "copy_subgraph": example_copy_and_subgraph,
    "ecommerce": example_ecommerce_system,
}


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        if example_name in EXAMPLES:
            EXAMPLES[example_name]()
        else:
            print(f"Unknown example: {example_name}")
            print(f"Available: {', '.join(EXAMPLES.keys())}")
            sys.exit(1)
    else:
        # Run all examples
        for name in EXAMPLES:
            EXAMPLES[name]()
            print()
            print()
