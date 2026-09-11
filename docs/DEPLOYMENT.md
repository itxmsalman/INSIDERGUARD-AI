# Deployment Guide

## Local deployment

```bash
source .venv/bin/activate
streamlit run app.py
```

The dashboard normally opens at:

`http://localhost:8501`

Stop it with `Ctrl+C`.

## GitHub

```bash
git init
git add .
git commit -m "Build INSIDERGUARD AI dashboard"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

Before pushing:

- Do not commit passwords or API keys.
- Do not commit private or restricted datasets.
- Review the README.
- Keep synthetic/demo results clearly labelled.

## Streamlit Community Cloud

A typical deployment flow is:

1. Push the repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create a new app from the repository.
4. Select `app.py` as the main file.
5. Deploy.

The app should install dependencies from `requirements.txt`.

If the deployment environment has a different Python version, pin versions in `requirements.txt` after testing.

## Proxmox deployment (optional)

Keep the MacBook as the primary development machine.

For a Linux deployment lab:

1. Create an Ubuntu VM on Proxmox.
2. Install Python and Git.
3. Clone the GitHub repository.
4. Create a virtual environment.
5. Install requirements.
6. Run Streamlit.
7. Access the VM from your LAN using its IP and port 8501.

Example:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd INSIDERGUARD-AI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0
```

Do not expose port 8501 directly to the public internet without authentication, access controls and a properly designed deployment.
