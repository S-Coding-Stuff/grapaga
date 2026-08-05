import torch


@torch.no_grad()
def evaluate_micro_f1(
    model: torch.nn.Module,
    loader,
    device: torch.device,
    threshold: float = 0.5,
) -> float:
    """Compute micro-F1 for multi-label node classification."""
    model.eval()

    true_positives = 0.0
    false_positives = 0.0
    false_negatives = 0.0

    for batch in loader:
        batch = batch.to(device)
        logits = model(batch.x, batch.edge_index)
        predictions = (logits.sigmoid() >= threshold).float()
        targets = batch.y.float()

        true_positives += (predictions * targets).sum().item()
        false_positives += (predictions * (1.0 - targets)).sum().item()
        false_negatives += ((1.0 - predictions) * targets).sum().item()

    denominator = (2.0 * true_positives) + false_positives + false_negatives
    if denominator == 0.0:
        return 0.0

    return (2.0 * true_positives) / denominator


@torch.no_grad()
def predict_logits(model: torch.nn.Module, loader, device: torch.device) -> list[torch.Tensor]:
    model.eval()
    outputs: list[torch.Tensor] = []

    for batch in loader:
        batch = batch.to(device)
        outputs.append(model(batch.x, batch.edge_index).cpu())

    return outputs
