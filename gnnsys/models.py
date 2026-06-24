import numpy as np
import torch
import torch_geometric.nn as gnn

class GCN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GCN, self).__init__()
        self.conv1 = gnn.GCNConv(input_dim, hidden_dim)
        self.conv2 = gnn.GCNConv(hidden_dim, output_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        return x
    
class LinkPredictionModel(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(LinkPredictionModel, self).__init__()
        self.gcn = GCN(input_dim, hidden_dim, output_dim)
        self.fc = torch.nn.Linear(2 * output_dim, 1)  # For link prediction

    def forward(self, data, edge_pairs):
        node_embeddings = self.gcn(data)
        edge_embeddings = torch.cat([node_embeddings[edge_pairs[:, 0]], node_embeddings[edge_pairs[:, 1]]], dim=1)
        return torch.sigmoid(self.fc(edge_embeddings))