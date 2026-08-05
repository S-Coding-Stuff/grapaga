from dataclasses import dataclass

from torch_geometric.datasets import PPI
from torch_geometric.loader import DataLoader

DEFAULT_PPI_ROOT = "data/ppi"


@dataclass(frozen=True)
class PPISplits:
    train: PPI
    val: PPI
    test: PPI


@dataclass(frozen=True)
class PPILoaders:
    train: DataLoader
    val: DataLoader
    test: DataLoader


def load_ppi_datasets(root: str = DEFAULT_PPI_ROOT) -> PPISplits:
    """Load the inductive PPI train/val/test splits."""
    return PPISplits(
        train=PPI(root=root, split="train"),
        val=PPI(root=root, split="val"),
        test=PPI(root=root, split="test"),
    )


def build_ppi_loaders(root: str = DEFAULT_PPI_ROOT, batch_size: int = 2) -> PPILoaders:
    """Create dataloaders for the standard PPI splits."""
    datasets = load_ppi_datasets(root=root)
    return PPILoaders(
        train=DataLoader(datasets.train, batch_size=batch_size, shuffle=True),
        val=DataLoader(datasets.val, batch_size=batch_size, shuffle=False),
        test=DataLoader(datasets.test, batch_size=batch_size, shuffle=False),
    )
