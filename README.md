# 🛡️ INSIDERGUARD AI

**Behavioural Security Intelligence Platform**

A small, professional-looking AI cybersecurity application built for practical learning and PhD preparation.

## What it demonstrates

- Python application structure
- Pandas data handling
- Scikit-learn Random Forest classification
- PyTorch neural-network baseline
- Side-by-side two-model comparison
- Model training and persistence
- Interactive prediction
- Streamlit dashboard development
- Basic model feature importance
- Automated tests
- Git/GitHub project organisation

## ⚠️ Important research note

The included dataset is **synthetic demonstration data**. The application is an educational prototype.

The current model output must NOT be interpreted as a real insider-threat assessment, employee risk score, or production security decision.

For research, replace the demo data with an appropriately obtained dataset and document preprocessing, licensing, ethics, experimental design and evaluation.

## Quick start - macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/train_all.py
python src/predict.py
streamlit run app.py
```

Open the browser URL shown by Streamlit, normally:

`http://localhost:8501`

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

```text
INSIDERGUARD-AI/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   ├── behavioural_demo.csv
│   └── README.md
├── src/
│   ├── model_utils.py
│   ├── train.py
│   └── predict.py
├── models/
├── notebooks/
│   └── 01_exploration.ipynb
├── tests/
│   └── test_pipeline.py
└── docs/
```

## Dashboard

The app contains:

- 🏠 Overview
- 🔍 Live Analysis
- 🚨 Alerts
- 🧠 Model Lab
- 📊 Dataset
- 🖥️ Terminal
- ⚙️ Settings

The visual language is inspired by modern SOC dashboards and Linux/terminal environments, while using original project branding.

## Model training

Run `python src/train_all.py` to retrain both the Random Forest and PyTorch baselines and save their model artefacts under `models/`. The bundled results are for the tiny synthetic demo dataset only and are not research or production performance.

## Future research direction

The project can later evolve toward:

1. PyTorch neural-network baseline
2. Explainable AI
3. Privacy-preserving ML
4. Federated learning
5. Real CERT insider-threat experiments

These later stages should be implemented only after the underlying concepts are understood.

## Supervisor handoff

Once you have personally learned and tested the project, publish the cleaned repository to GitHub and share the repository link with Dr Yanran.

