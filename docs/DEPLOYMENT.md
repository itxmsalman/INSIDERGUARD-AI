# Deployment Guide

This guide describes how to run and deploy INSIDERGUARD AI in local, cloud-hosted, and virtualised development environments.

INSIDERGUARD AI is currently a research and learning prototype and is not intended for production security decision-making.

---

## Local deployment

Clone the repository:

```bash
git clone https://github.com/itxmsalman/INSIDERGUARD-AI.git
cd INSIDERGUARD-AI
```

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Train the available machine-learning models:

```bash
python src/train_all.py
```

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

The dashboard normally opens at:

`http://localhost:8501`

Stop the application with:

`Ctrl+C`

---

## Updating the GitHub repository

The public repository is available at:

`https://github.com/itxmsalman/INSIDERGUARD-AI`

After making local changes, check the repository status:

```bash
git status
```

Stage the changes:

```bash
git add .
```

Create a commit:

```bash
git commit -m "Update INSIDERGUARD AI"
```

Push the changes to GitHub:

```bash
git push
```

Before pushing changes, verify that the repository does not contain:

- Passwords
- API keys
- Authentication tokens
- Personal or confidential information
- Private or restricted datasets
- Raw CERT Insider Threat Dataset files
- Local virtual environments
- Temporary development files
- Machine-specific configuration files

Synthetic or demonstration data should always remain clearly labelled.

---

## Streamlit Community Cloud

INSIDERGUARD AI may be deployed to Streamlit Community Cloud for demonstration purposes.

A typical deployment process is:

1. Push the latest version of the project to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create a new application.
4. Select the `itxmsalman/INSIDERGUARD-AI` repository.
5. Select `app.py` as the main application file.
6. Configure the deployment environment if required.
7. Deploy the application.

Dependencies should be installed automatically from:

`requirements.txt`

If compatibility issues occur because of differences in Python or package versions, tested dependency versions can be pinned in `requirements.txt`.

---

## Proxmox deployment

INSIDERGUARD AI can also be deployed inside an Ubuntu virtual machine hosted on Proxmox VE.

This provides a controlled environment for infrastructure experimentation, cybersecurity-lab work, and reproducibility.

### Suggested environment

- Proxmox VE
- Ubuntu Server virtual machine
- Python 3
- Git
- Python virtual environment
- Streamlit
- Trusted LAN or private network connectivity

### Install required packages

On the Ubuntu virtual machine:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

Clone the repository:

```bash
git clone https://github.com/itxmsalman/INSIDERGUARD-AI.git
cd INSIDERGUARD-AI
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

Train the models:

```bash
python src/train_all.py
```

Start the Streamlit application:

```bash
streamlit run app.py --server.address 0.0.0.0
```

The dashboard can then be accessed from another device on the same trusted network using:

`http://<VM-IP-ADDRESS>:8501`

Replace `<VM-IP-ADDRESS>` with the IP address assigned to the Ubuntu virtual machine.

---

## Security considerations

Do not expose Streamlit port `8501` directly to the public internet without appropriate security controls.

A production-style deployment would require additional safeguards such as:

- Authentication
- Authorisation
- HTTPS/TLS
- Firewall rules
- Reverse proxy configuration
- Network segmentation
- Secure secret management
- Access logging
- Monitoring
- Patch management
- Backup and recovery procedures

The current application is not designed as a production insider-threat monitoring platform.

---

## Data considerations

The bundled `behavioural_demo.csv` file contains synthetic demonstration data.

It is not the CERT Insider Threat Dataset.

Any model results generated from the synthetic dataset are for demonstration purposes only and should not be interpreted as real-world or research performance.

Raw third-party research datasets, including the CERT Insider Threat Dataset, should remain outside the public GitHub repository unless redistribution is explicitly permitted by the dataset provider or licence.

Future experiments involving real behavioural data should consider:

- Data minimisation
- Privacy
- Lawful data processing
- Access control
- Ethical approval
- Secure storage
- Data retention
- Auditability
- Organisational governance

---

## Reproducibility

For research-oriented experimentation, relevant environment and experiment details should be documented.

These may include:

- Python version
- Package versions
- Dataset version
- Dataset preprocessing
- Model configuration
- Training parameters
- Random seeds where applicable
- Evaluation metrics
- Deployment environment
- Hardware or virtual-machine configuration

Recording these details helps support reproducibility and comparison across experimental runs.

---

## Deployment status

The current project supports:

- Local macOS/Linux execution
- GitHub-based version control
- Streamlit dashboard execution
- Streamlit Community Cloud deployment
- Optional Proxmox-hosted Ubuntu deployment

Further deployment automation may be added as the project develops.

---

## Responsible use

INSIDERGUARD AI is an educational and research-development prototype.

It should not be used to assess real employees or make employment, disciplinary, monitoring, or operational security decisions about individuals without appropriate validation, governance, privacy safeguards, ethical review, and organisational approval.

The project is intended to support learning, experimentation, and future research into AI-assisted insider-threat detection and behavioural cybersecurity.
