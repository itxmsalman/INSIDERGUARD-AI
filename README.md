# 🛡️ INSIDERGUARD AI

**Behavioural Security Intelligence Platform**

INSIDERGUARD AI is an experimental cybersecurity and machine-learning prototype developed to explore AI-assisted insider-threat analysis using behavioural activity data.

The project combines traditional machine learning, a neural-network baseline, interactive analysis, and a SOC-inspired dashboard within a reproducible Python workflow.

---

## What it demonstrates

- Python application structure
- Pandas-based data processing
- Scikit-learn Random Forest classification
- PyTorch neural-network baseline
- Side-by-side model comparison
- Model training and persistence
- Interactive behavioural-risk prediction
- Streamlit dashboard development
- Basic feature-importance analysis
- Automated testing
- Git/GitHub project organisation

---

## ⚠️ Research and data notice

The dataset included in this repository is **synthetic demonstration data** created for development, experimentation, and learning purposes.

The current model outputs must **not** be interpreted as real insider-threat assessments, employee risk scores, or production security decisions.

Future research experiments should use appropriately obtained datasets with clearly documented preprocessing, licensing, ethical considerations, experimental design, and evaluation methodology.

Raw third-party research datasets, including the CERT Insider Threat Dataset, should remain outside this public repository unless redistribution is explicitly permitted.

---

## Quick start

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/train_all.py
python src/predict.py
streamlit run app.py
```

The Streamlit dashboard normally opens at:

`http://localhost:8501`

---

## Run tests

```bash
python -m unittest discover -s tests -v
```

---

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
│   ├── train_all.py
│   └── predict.py
├── models/
├── notebooks/
│   └── 01_exploration.ipynb
├── tests/
│   └── test_pipeline.py
└── docs/
    ├── DEPLOYMENT.md
    ├── RESEARCH_ROADMAP.md
    └── TECHNICAL_ROADMAP.md
```

---

## Dashboard

The application contains:

- 🏠 Overview
- 🔍 Live Analysis
- 🚨 Alerts
- 🧠 Model Lab
- 📊 Dataset
- 🖥️ Terminal
- ⚙️ Settings

The interface draws inspiration from contemporary Security Operations Centre (SOC) dashboards and terminal-based security environments while using original INSIDERGUARD AI branding.

---

## Machine-learning models

The current prototype compares two baseline approaches.

### Random Forest

A Scikit-learn ensemble classifier used as the traditional machine-learning baseline.

### PyTorch Neural Network

A small neural-network classifier used to explore a deep-learning approach using the same behavioural feature set.

To retrain both models, run:

```bash
python src/train_all.py
```

Generated model artefacts are stored under:

```text
models/
```

Results generated using the bundled synthetic dataset are demonstration results only and should not be interpreted as research or real-world performance.

---

## Behavioural features

The demonstration workflow uses behavioural activity features such as:

- After-hours login activity
- File-access activity
- Email activity
- Device activity
- Web activity

These features are used to demonstrate the machine-learning workflow and do not represent a validated real-world insider-risk model.

---

## Model workflow

```text
Behavioural data
        ↓
Data preprocessing
        ↓
Feature selection
        ↓
Train/test split
        ↓
┌─────────────────────────────┐
│       Model comparison      │
│                             │
│  Random Forest              │
│  PyTorch Neural Network     │
└─────────────────────────────┘
        ↓
Model evaluation
        ↓
Saved model artefacts
        ↓
Interactive prediction
        ↓
Streamlit dashboard
```

---

## Evaluation

The project supports evaluation using common classification metrics including:

- Precision
- Recall
- F1-score
- Confusion matrix
- Prediction output
- Basic feature importance

Any reported results produced from the bundled synthetic dataset should be treated only as technical demonstration results.

---

## Data

`data/behavioural_demo.csv` contains synthetic demonstration data created for the INSIDERGUARD AI prototype.

It is **not** the CERT Insider Threat Dataset.

Any model results produced using this file are for demonstration purposes only and must not be interpreted as real-world or validated research performance.

For future research, datasets such as the CERT Insider Threat Dataset should be obtained from authorised sources. Raw research data should remain outside the public GitHub repository unless redistribution is explicitly permitted by the dataset provider or licence.

The public repository is intended to contain code, documentation, reproducible workflows, and appropriately shareable demonstration data only.

See `data/README.md` for further information about the demonstration dataset.

---

## Research direction

Future development may investigate:

1. Explainable AI using methods such as SHAP or LIME
2. Privacy-preserving machine learning
3. Federated learning across distributed organisational environments
4. More advanced behavioural feature engineering
5. Experiments using appropriately obtained CERT insider-threat data
6. Evaluation under realistic class imbalance and non-IID conditions
7. Analyst-oriented explanations and decision-support mechanisms
8. Integration with SIEM and security-monitoring environments

These extensions are intended as future research directions rather than capabilities claimed by the current prototype.

---

## Documentation

Additional project documentation is available under the `docs/` directory:

- `RESEARCH_ROADMAP.md` — current implementation, planned research extensions, limitations, and longer-term objectives
- `TECHNICAL_ROADMAP.md` — technical development across Python, data processing, machine learning, evaluation, and application development
- `DEPLOYMENT.md` — local, Streamlit, and Proxmox deployment guidance, including security and reproducibility considerations

---

## Project status

This repository contains a research and learning prototype developed to explore AI-based insider-threat detection using behavioural activity data.

The current implementation demonstrates an end-to-end workflow involving data preparation, model training, model comparison, evaluation, prediction, and interactive visualisation.

The project will continue to evolve as part of my broader research development in artificial intelligence, cybersecurity, insider risk, and socio-technical security.

---

## Limitations

The current version has several important limitations:

- It uses synthetic demonstration data
- It has not been validated in a real organisational environment
- It is not a production security system
- It does not provide a validated employee risk score
- The neural-network model is a baseline implementation
- Current evaluation results are not representative of operational performance
- Real-world deployment would require stronger validation, privacy safeguards, governance, and ethical review

---

## Responsible use

INSIDERGUARD AI is intended for educational, experimental, and research-development purposes.

It should not be used to make employment, disciplinary, monitoring, or operational security decisions about real individuals.

Any future research involving real behavioural or employee data should include appropriate ethical review, privacy safeguards, lawful data processing, transparency, access controls, and organisational governance.

---

## Technologies

- Python
- Pandas
- Scikit-learn
- PyTorch
- Streamlit
- Jupyter Notebook
- Git
- GitHub

---

## Author

**Muhammad Salman**

Research interests include:

- Artificial Intelligence
- Cybersecurity
- Insider Threat Detection
- Behavioural Security
- Cyber Resilience
- Socio-Technical Security
- Explainable AI
- Privacy-Preserving Machine Learning

---

## Research profile

INSIDERGUARD AI supports my broader academic interest in understanding how artificial intelligence and behavioural data can contribute to cybersecurity research while maintaining responsible, transparent, and privacy-aware approaches to security analysis.
