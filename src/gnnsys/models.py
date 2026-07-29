"""Simple Numpy GNN"""
import numpy as np
class SimpleGNN:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        
        np.random.seed(42)
        
        # Network Message Weights
        self.W_message = np.random.randn(input_dim, hidden_dim) * 0.1 # Not exactly a good way to initialise
        self.b_message = np.zeros(hidden_dim)
        # Output Weights
        self.W_update = np.random.randn(input_dim + hidden_dim, output_dim) * 0.1
        self.b_update = np.zeros(output_dim)
        
    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    @staticmethod
    def relu(x):
        return np.maximum(0, x)
    
    def create_message(self, node_features):
        messages = np.dot(node_features, self.W_message) + self.b_message
        messages = self.relu(messages)
        return messages
    
    def aggregate_messages(self, messages, adjacency_mat):
        aggregated = np.dot(adjacency_mat, messages)
        return aggregated
    
    def update_nodes(self, node_features, aggregate_messages):
        combined = np.concatenate([node_features, aggregate_messages], axis=1)
        updated = np.dot(combined, self.W_update) + self.b_update
        updated = self.sigmoid(updated)
        return updated
    
    def forward(self, node_features, adjacency_mat):
        messages = self.create_message(node_features)
        aggregated = self.aggregate_messages(messages, adjacency_mat)
        updated_features = self.update_nodes(node_features, aggregated)
        return updated_features, messages, aggregated