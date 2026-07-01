import torch
from torch_geometric.data import Data
from gnnsys.models import LinkPredictionModel
import yaml
import argparse

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def train_model(model, data, edge_pairs, optimiser, loss_fn, epochs):
    model.train()
    for epoch in range(epochs):
        optimiser.zero_grad()
        output = model(data, edge_pairs)
        loss = loss_fn(output)
        loss.backward()
        optimiser.step()
        optimiser.zero_grad()

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    args = parser.parse_args()

    config = load_config(args.config)