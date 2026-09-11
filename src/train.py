from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from model_utils import train_model, save_model  # noqa: E402


def main() -> None:
    model, metrics = train_model()
    path = save_model(model)

    print("=== INSIDERGUARD AI :: MODEL TRAINING ===")
    print(f"Dataset rows : {metrics['dataset_rows']}")
    print(f"Train rows   : {metrics['train_rows']}")
    print(f"Test rows    : {metrics['test_rows']}")
    print(f"Accuracy     : {metrics['accuracy']:.2f}")
    print("\n=== Classification Report ===")
    print(metrics["classification_report"])
    print("=== Confusion Matrix ===")
    print(metrics["confusion_matrix"])
    print(f"\nSaved model: {path}")


if __name__ == "__main__":
    main()
