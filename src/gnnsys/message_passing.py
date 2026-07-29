import numpy as np
from models import SimpleGNN

def create_network_dataset():
    """
    Graph: Agent Network
    Node Features: [agent_id, x_pos, y_pos, speed]
    A1 (0) --- A2 (1)
    |           |
    A3 (2) --- A4 (3)
    """
    
    node_features = np.array([
        [0, 0, 4],
        [5, 10, 3],
        [2, 6, 9],
        [-2, 3, 5]
    ], dtype=np.float32)
    
    node_features = (node_features - node_features.min(axis=0)) / (node_features.max(axis=0) - node_features.min(axis=0))
    
    adjacency_mat = np.array([
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0]
    ])
    names = ["A1", "A2", "A3", "A4"]
    return node_features, adjacency_mat, names

def demonstrate():
    
    print("=== Message Passing Demo ===")
    node_features, adjacency_mat, names = create_network_dataset()
    print("Node features:")
    for i, name in enumerate(names):
        print(f"{name:8}: {node_features[i]}")
    gnn = SimpleGNN(input_dim=3, hidden_dim=6, output_dim=2)
    
    print("\n" + "="*50)
    print("MESSAGE PASSING PROCESS")