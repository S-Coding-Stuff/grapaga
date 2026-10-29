import argparse
from dataclasses import dataclass

import torch

from gnnsys.data import DEFAULT_PPI_ROOT, build_ppi_loaders
from gnnsys.eval import evaluate_micro_f1
from gnnsys.models import GraphSAGE


@dataclass
class TrainingConfig:
    """Configuration for training GraphSAGE on the PPI dataset."""

    root: str = DEFAULT_PPI_ROOT
    hidden_channels: int = 256
    num_layers: int = 3
    dropout: float = 0.2
    learning_rate: float = 0.005
    weight_decay: float = 0.0
    batch_size: int = 2
    epochs: int = 50
    threshold: float = 0.5


def train_one_epoch(
    model: torch.nn.Module,
    loader,
    optimizer: torch.optim.Optimizer,
    criterion: torch.nn.Module,
    device: torch.device,
) -> float:
    """Train the model for one epoch."""
    model.train()
    total_loss = 0.0

    for batch in loader:
        batch = batch.to(device)
        optimizer.zero_grad()

        logits = model(batch.x, batch.edge_index)
        loss = criterion(logits, batch.y.float())

        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    return total_loss / len(loader)


def fit_ppi(config: TrainingConfig) -> tuple[torch.nn.Module, float]:
    """Train the GraphSAGE model on the PPI dataset."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loaders = build_ppi_loaders(config.root, config.batch_size)
    train_loader = loaders.train
    val_loader = loaders.val
    test_loader = loaders.test

    model = GraphSAGE(
        in_channels=train_loader.dataset.num_features,
        out_channels=train_loader.dataset.num_classes,
        hidden_channels=config.hidden_channels,
        num_layers=config.num_layers,
        dropout=config.dropout,
    ).to(device)

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay,
    )
    criterion = torch.nn.BCEWithLogitsLoss()

    best_state = None
    best_val_f1 = 0.0

    for epoch in range(1, config.epochs + 1):
        loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
        val_f1 = evaluate_micro_f1(model, val_loader, device, threshold=config.threshold)

        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            best_state = {key: value.detach().cpu() for key, value in model.state_dict().items()}

        print(f"epoch={epoch:03d} loss={loss:.4f} val_micro_f1={val_f1:.4f}")

    if best_state is not None:
        model.load_state_dict(best_state)

    test_f1 = evaluate_micro_f1(model, test_loader, device, threshold=config.threshold)
    print(f"test_micro_f1={test_f1:.4f}")
    return model, test_f1


def parse_args() -> TrainingConfig:
    """Parse command-line arguments for training GraphSAGE on the PPI dataset."""
    parser = argparse.ArgumentParser(description="Train GraphSAGE on the PPI dataset.")
    parser.add_argument("--root", default=DEFAULT_PPI_ROOT)
    parser.add_argument("--hidden-channels", type=int, default=256)
    parser.add_argument("--num-layers", type=int, default=3)
    parser.add_argument("--dropout", type=float, default=0.2)
    parser.add_argument("--learning-rate", type=float, default=0.005)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    return TrainingConfig(
        root=args.root,
        hidden_channels=args.hidden_channels,
        num_layers=args.num_layers,
        dropout=args.dropout,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        batch_size=args.batch_size,
        epochs=args.epochs,
        threshold=args.threshold,
    )


def main() -> None:
    """Train GraphSAGE on the PPI dataset."""
    config = parse_args()
    fit_ppi(config)


if __name__ == "__main__":
    main()
