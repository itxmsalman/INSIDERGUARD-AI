from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from model_utils import load_model, FEATURES  # noqa: E402


def predict_activity(values: dict):
    model, features = load_model()
    frame = pd.DataFrame([values], columns=features)
    prediction = int(model.predict(frame)[0])
    probabilities = model.predict_proba(frame)[0]
    class_1_index = list(model.classes_).index(1)
    probability = float(probabilities[class_1_index])
    return prediction, probability


def main() -> None:
    prompts = {
        "after_hours_logins": "After-hours logins: ",
        "file_access_count": "File access count: ",
        "email_activity": "Email activity: ",
        "device_activity": "Device activity: ",
        "web_activity": "Web activity: ",
    }

    values = {}
    for key, prompt in prompts.items():
        while True:
            try:
                values[key] = float(input(prompt))
                break
            except ValueError:
                print("Please enter a number.")

    prediction, probability = predict_activity(values)
    print("\n=== Prediction Result ===")
    print(f"Predicted class: {prediction}")
    print(f"Class-1 probability: {probability:.3f}")


if __name__ == "__main__":
    main()
