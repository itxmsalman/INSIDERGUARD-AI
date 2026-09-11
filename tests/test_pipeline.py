import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from model_utils import FEATURES, TARGET, load_data, load_model  # noqa: E402


class TestPipeline(unittest.TestCase):
    def test_dataset_schema(self):
        df = load_data()
        self.assertTrue(set(FEATURES + [TARGET]).issubset(df.columns))
        self.assertEqual(len(df), 19)

    def test_model_prediction(self):
        model, features = load_model()
        import pandas as pd
        sample = pd.DataFrame([[1, 3, 4, 0, 5]], columns=features)
        prediction = model.predict(sample)
        self.assertIn(int(prediction[0]), [0, 1])
        self.assertEqual(list(features), FEATURES)

    def test_probability(self):
        model, features = load_model()
        import pandas as pd
        sample = pd.DataFrame([[6, 19, 22, 5, 30]], columns=features)
        probabilities = model.predict_proba(sample)
        self.assertEqual(probabilities.shape, (1, 2))
        self.assertAlmostEqual(float(probabilities.sum()), 1.0, places=6)

    def test_pytorch_file_exists(self):
        self.assertTrue((ROOT / "models" / "insider_threat_pytorch.pt").exists())


if __name__ == "__main__":
    unittest.main()
