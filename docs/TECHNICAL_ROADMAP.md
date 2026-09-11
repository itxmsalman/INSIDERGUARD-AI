# Technical Roadmap

This roadmap describes the technical development path for INSIDERGUARD AI, from the current baseline implementation toward more advanced research capabilities.

## Python and software foundation

Core development areas include:

- Python project structure
- Functions and reusable modules
- Data structures
- Exception handling
- Package management
- Testing
- Code organisation
- Version control with Git

## Data processing

The project uses behavioural activity data and will continue to develop around:

- CSV and structured datasets
- Pandas DataFrames
- Data cleaning
- Feature selection
- Behavioural feature engineering
- Train/test preparation
- Data validation
- Reproducible preprocessing pipelines

## Machine learning

The current machine-learning workflow includes:

- Feature matrix and target labels
- Train/test splitting
- Random Forest classification
- PyTorch neural-network baseline
- Model training and prediction
- Prediction probabilities
- Precision
- Recall
- F1-score
- Confusion-matrix analysis
- Model comparison

## Application development

The Streamlit application provides an interactive interface for exploring the prototype.

Development areas include:

- Interactive widgets
- Session state
- Data visualisation
- DataFrame presentation
- Model outputs
- Dashboard navigation
- Model comparison
- User-facing explanations

## Model evaluation

Further development will focus on improving experimental evaluation through:

- Class-specific precision and recall
- F1-score analysis
- False-positive and false-negative analysis
- Class imbalance
- Cross-validation
- Baseline comparison
- Reproducibility across experiments

## Research extensions

After the baseline workflow is sufficiently understood and validated, future work may investigate:

- Explainable AI
- SHAP and LIME
- Federated learning
- Privacy-preserving machine learning
- Non-IID distributed datasets
- More advanced PyTorch models
- Real CERT insider-threat experiments
- Analyst-oriented decision support
- Integration with SIEM and security-monitoring environments

## AI development

Broader technical development may also include:

- Large Language Models
- Hugging Face
- AI agents
- Model deployment
- Responsible AI
- Human-AI interaction

These areas are complementary development directions and are not claimed as capabilities of the current INSIDERGUARD AI prototype.

## Development objective

The objective is to progress from a reproducible machine-learning baseline toward a research-oriented insider-threat analysis framework while maintaining clear evaluation, responsible data handling, transparency and reproducibility.
