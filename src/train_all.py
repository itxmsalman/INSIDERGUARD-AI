from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd
import joblib
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from model_utils import FEATURES, TARGET, load_data, train_model, save_model

class InsiderThreatNN(nn.Module):
    def __init__(self, input_features: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_features, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 2),
        )
    def forward(self, x):
        return self.network(x)

def train_pytorch():
    torch.manual_seed(42)
    np.random.seed(42)
    df = load_data()
    X = df[FEATURES].astype(np.float32).values
    y = df[TARGET].astype(np.int64).values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )

    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    std[std == 0] = 1.0
    X_train = (X_train - mean) / std
    X_test = (X_test - mean) / std

    xt = torch.tensor(X_train, dtype=torch.float32)
    yt = torch.tensor(y_train, dtype=torch.long)

    model = InsiderThreatNN(len(FEATURES))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.CrossEntropyLoss()

    model.train()
    for _ in range(500):
        optimizer.zero_grad()
        logits = model(xt)
        loss = loss_fn(logits, yt)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        logits = model(torch.tensor(X_test, dtype=torch.float32))
        probs = torch.softmax(logits, dim=1).numpy()
        pred = np.argmax(probs, axis=1)

    metrics = {
        'accuracy': float(accuracy_score(y_test, pred)),
        'report': classification_report(y_test, pred, zero_division=0),
        'matrix': confusion_matrix(y_test, pred).tolist(),
        'train_rows': int(len(X_train)),
        'test_rows': int(len(X_test)),
    }
    path = ROOT / 'models' / 'insider_threat_pytorch.pt'
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        'state_dict': model.state_dict(),
        'features': FEATURES,
        'mean': mean,
        'std': std,
    }, path)
    return metrics, path

def main():
    rf_model, rf_metrics = train_model()
    rf_path = save_model(rf_model)
    pt_metrics, pt_path = train_pytorch()

    output = {
        'dataset_rows': int(len(load_data())),
        'random_forest': {
            'accuracy': rf_metrics['accuracy'],
            'train_rows': rf_metrics['train_rows'],
            'test_rows': rf_metrics['test_rows'],
            'report': rf_metrics['classification_report'],
            'matrix': rf_metrics['confusion_matrix'],
        },
        'pytorch': pt_metrics,
    }
    metrics_path = ROOT / 'models' / 'training_metrics.json'
    metrics_path.write_text(json.dumps(output, indent=2), encoding='utf-8')

    print('=== INSIDERGUARD AI :: RETRAIN ALL ===')
    print(f'Dataset rows          : {output["dataset_rows"]}')
    print(f'Random Forest model   : {rf_path}')
    print(f'Random Forest accuracy: {rf_metrics["accuracy"]:.2f}')
    print(f'PyTorch model         : {pt_path}')
    print(f'PyTorch test accuracy : {pt_metrics["accuracy"]:.2f}')
    print(f'Metrics file          : {metrics_path}')
    print('\nNOTE: results are from the tiny synthetic demonstration dataset and are not research or production performance.')

if __name__ == '__main__':
    main()
