from datetime import datetime
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import streamlit as st
import torch
import torch.nn as nn

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from model_utils import (  # noqa: E402
    FEATURES,
    TARGET,
    load_data,
    load_model,
    train_model,
    save_model,
)

st.set_page_config(
    page_title="INSIDERGUARD AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Theme
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --bg:#070b14; --panel:#0d1422; --panel2:#101a2b; --border:#20304a;
        --cyan:#27e6d6; --blue:#4da3ff; --green:#39d98a; --amber:#f6c85f;
        --red:#ff6577; --text:#edf4ff; --muted:#8ea2bd;
    }
    .stApp{background:var(--bg);color:var(--text)}
    .block-container{padding-top:1.2rem;padding-bottom:1.2rem;max-width:1550px}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#07101d 0%,#0a1322 100%);border-right:1px solid var(--border)}
    [data-testid="stSidebar"] *{color:var(--text)}
    .brand{padding:6px 0 16px}.brand-title{font-size:24px;font-weight:950;letter-spacing:1px;white-space:nowrap}.brand-title span{color:var(--cyan)}
    .brand-sub{color:var(--muted);font-size:9px;letter-spacing:1.1px;white-space:nowrap}
    .topbar{background:linear-gradient(135deg,#0b1627 0%,#111d33 100%);border:1px solid var(--border);border-radius:15px;padding:15px 19px;margin-bottom:14px;box-shadow:0 12px 32px rgba(0,0,0,.18)}
    .top-row{display:flex;align-items:center;justify-content:space-between;gap:18px}.top-title{font-size:28px;font-weight:950;letter-spacing:1px}.top-sub{color:var(--muted);font-size:11px;letter-spacing:.8px;margin-top:2px}
    .status-pill{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;border:1px solid #2b4a59;background:#0a1a22;color:#d7f9ed;font-size:11px;font-weight:850;white-space:nowrap}
    .dot{width:9px;height:9px;border-radius:50%;display:inline-block}.dot-green{background:var(--green);box-shadow:0 0 11px rgba(57,217,138,.55)}
    .section-label{color:var(--cyan);font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-weight:900;letter-spacing:1.1px;margin:8px 0 10px;font-size:13px}
    .metric-card,.card{background:linear-gradient(180deg,var(--panel) 0%,#0b1320 100%);border:1px solid var(--border);border-radius:14px;padding:15px 17px;box-shadow:inset 0 1px 0 rgba(255,255,255,.02)}
    .metric-card{min-height:96px}.metric-label{color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:1px}.metric-value{font-size:27px;font-weight:950;margin-top:4px}.metric-green{color:var(--green)}.metric-red{color:var(--red)}.metric-blue{color:var(--blue)}.metric-cyan{color:var(--cyan)}
    .card-title{font-size:14px;font-weight:900;letter-spacing:.25px}.muted{color:var(--muted);font-size:11px}
    .result-low,.result-mid,.result-high{border-radius:16px;padding:20px 22px;min-height:175px}.result-low{border:1px solid rgba(57,217,138,.45);background:linear-gradient(135deg,rgba(57,217,138,.10),rgba(13,20,34,.94))}.result-mid{border:1px solid rgba(246,200,95,.50);background:linear-gradient(135deg,rgba(246,200,95,.10),rgba(13,20,34,.94))}.result-high{border:1px solid rgba(255,101,119,.48);background:linear-gradient(135deg,rgba(255,101,119,.10),rgba(13,20,34,.94))}.result-title{font-size:20px;font-weight:950;letter-spacing:.7px}.result-score{font-size:40px;font-weight:950;margin-top:8px}.result-meta{color:var(--muted);font-size:11px;margin-top:5px}
    .terminal{background:#04070c;border:1px solid #21314a;border-radius:12px;padding:13px 15px;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;color:#cfe8e4;line-height:1.62;min-height:130px}.term-green{color:var(--green)}.term-cyan{color:var(--cyan)}.term-blue{color:var(--blue)}.term-amber{color:var(--amber)}.term-red{color:var(--red)}
    .warning-strip{background:rgba(246,200,95,.09);border:1px solid rgba(246,200,95,.25);color:#f9efc1;border-radius:10px;padding:9px 12px;font-size:11px;margin-top:10px}
    div.stButton>button{width:100%;border-radius:10px;border:1px solid #2d7180;background:linear-gradient(100deg,#103b46,#173b61);color:#fff;font-weight:900;min-height:42px}div.stButton>button:hover{border-color:var(--cyan);box-shadow:0 0 16px rgba(39,230,214,.15);color:#fff}
    .stNumberInput input{background:#0a111d!important;color:var(--text)!important;border:1px solid #263a56!important;border-radius:9px!important}.stNumberInput label{color:#dfe8f7!important;font-size:11px!important;font-weight:800!important}.stSelectbox label{color:#dfe8f7!important;font-size:11px!important;font-weight:800!important}
    footer{visibility:hidden}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Data + Random Forest
# -----------------------------------------------------------------------------
df = load_data()
rf_model, features = load_model()
PYTORCH_MODEL_PATH = ROOT / "models" / "insider_threat_pytorch.pt"

@st.cache_data(show_spinner=False)
def get_demo_metrics():
    _, metrics = train_model()
    return metrics

metrics = get_demo_metrics()

# -----------------------------------------------------------------------------
# PyTorch baseline
# -----------------------------------------------------------------------------
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


@st.cache_resource(show_spinner="Loading PyTorch baseline...")
def get_pytorch_model():
    if not PYTORCH_MODEL_PATH.exists():
        st.warning("PyTorch model file not found. Run: python src/train_all.py")
        raise FileNotFoundError(PYTORCH_MODEL_PATH)
    bundle = torch.load(PYTORCH_MODEL_PATH, map_location="cpu", weights_only=False)
    model = InsiderThreatNN(len(FEATURES))
    model.load_state_dict(bundle["state_dict"])
    model.eval()
    mean = np.asarray(bundle["mean"], dtype=np.float32)
    std = np.asarray(bundle["std"], dtype=np.float32)
    return model, mean, std

def pytorch_predict(values: dict):
    model, mean, std = get_pytorch_model()
    x = np.array([[values[f] for f in FEATURES]], dtype=np.float32)
    xs = (x - mean) / std

    model.eval()
    with torch.no_grad():
        logits = model(torch.tensor(xs, dtype=torch.float32))
        probs = torch.softmax(logits, dim=1).numpy()[0]

    prediction = int(np.argmax(probs))
    return prediction, float(probs[1])

# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
def init_state():
    defaults = {
        "after_hours": 3.0,
        "file_access": 10.0,
        "email_activity": 12.0,
        "device_activity": 2.0,
        "web_activity": 15.0,
        "selected_model": "🔬 Compare Both",
        "last_result": None,
        "analysis_count": 0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def load_low_demo():
    st.session_state.after_hours = 1.0
    st.session_state.file_access = 3.0
    st.session_state.email_activity = 4.0
    st.session_state.device_activity = 0.0
    st.session_state.web_activity = 5.0


def load_high_demo():
    st.session_state.after_hours = 6.0
    st.session_state.file_access = 19.0
    st.session_state.email_activity = 22.0
    st.session_state.device_activity = 5.0
    st.session_state.web_activity = 30.0


init_state()

# Sidebar
st.sidebar.markdown(
    '<div class="brand"><div class="brand-title">🛡️ <span>INSIDERGUARD</span> AI</div><div class="brand-sub">BEHAVIOURAL SECURITY INTELLIGENCE</div></div>',
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "NAVIGATION",
    ["🏠 Overview", "🔍 Live Analysis", "🚨 Alerts", "🧠 Model Lab", "📊 Dataset", "🖥️ Terminal", "⚙️ Settings"],
)
st.sidebar.markdown("---")
st.sidebar.markdown("**SYSTEM**")
st.sidebar.markdown("🟢 RF model: Online")
st.sidebar.markdown("🧠 PyTorch model: Online")
st.sidebar.markdown(f"📁 Dataset: {len(df)} demo records")
st.sidebar.markdown("🧪 Mode: Educational Prototype")

# Header
st.markdown(
    '<div class="topbar"><div class="top-row"><div><div class="top-title">🛡️ INSIDERGUARD AI</div><div class="top-sub">AI-POWERED BEHAVIOURAL SECURITY INTELLIGENCE CONSOLE</div></div><div class="status-pill"><span class="dot dot-green"></span> MODELS ONLINE • RF + PYTORCH</div></div></div>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Overview
# -----------------------------------------------------------------------------
if page == "🏠 Overview":
    st.markdown('<div class="section-label">$ SECURITY OVERVIEW</div>', unsafe_allow_html=True)
    low = int((df[TARGET] == 0).sum())
    high = int((df[TARGET] == 1).sum())
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("📡 Demo Events", str(len(df)), "metric-blue"),
        ("🟢 Lower Class", str(low), "metric-green"),
        ("🔴 Higher Class", str(high), "metric-red"),
        ("🎯 RF Demo Accuracy", f"{metrics['accuracy']*100:.1f}%", "metric-cyan"),
    ]
    for col, (label, value, cls) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value {cls}">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    a, b = st.columns([1.6, 1])
    with a:
        st.markdown('<div class="section-label">$ BEHAVIOURAL ACTIVITY</div>', unsafe_allow_html=True)
        chart = df[FEATURES].copy()
        chart.columns = ["After-hours", "File access", "Email", "Device", "Web"]
        st.line_chart(chart, height=250)
    with b:
        st.markdown('<div class="section-label">$ CLASS DISTRIBUTION</div>', unsafe_allow_html=True)
        counts = df[TARGET].value_counts().reindex([0, 1]).fillna(0)
        counts.index = ["Lower-risk demo", "Higher-risk demo"]
        st.bar_chart(counts, height=250)

    st.markdown('<div class="section-label">$ MODEL FEATURE IMPORTANCE</div>', unsafe_allow_html=True)
    imp = pd.Series(
        rf_model.feature_importances_,
        index=["🌙 After-hours", "📁 File access", "✉️ Email", "💻 Device", "🌐 Web"],
    ).sort_values(ascending=False)
    st.bar_chart(imp, height=220)

    st.markdown('<div class="section-label">$ SYSTEM CONSOLE</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="terminal"><div><span class="term-green">[OK]</span> Random Forest model loaded</div><div><span class="term-green">[OK]</span> PyTorch neural-network baseline ready</div><div><span class="term-blue">[INFO]</span> {len(FEATURES)} behavioural features available</div><div><span class="term-amber">[NOTE]</span> Demo dataset only</div></div>',
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Live Analysis - BOTH MODELS
# -----------------------------------------------------------------------------
elif page == "🔍 Live Analysis":
    st.markdown('<div class="section-label">$ LIVE BEHAVIOURAL ANALYSIS</div>', unsafe_allow_html=True)
    left, right = st.columns([1, 1.22], gap="large")

    with left:
        st.markdown(
            '<div class="card"><div class="card-title">📥 ACTIVITY INPUT</div><div class="muted">Run the same behavioural vector through Random Forest, PyTorch, or both.</div></div>',
            unsafe_allow_html=True,
        )

        st.number_input("🌙 After-hours logins", min_value=0.0, step=1.0, key="after_hours")
        st.number_input("📁 File access count", min_value=0.0, step=1.0, key="file_access")
        st.number_input("✉️ Email activity", min_value=0.0, step=1.0, key="email_activity")
        st.number_input("💻 Device activity", min_value=0.0, step=1.0, key="device_activity")
        st.number_input("🌐 Web activity", min_value=0.0, step=1.0, key="web_activity")

        st.selectbox(
            "🤖 CHOOSE AI MODEL",
            ["🌲 Random Forest", "🧠 PyTorch Neural Network", "🔬 Compare Both"],
            key="selected_model",
        )

        demo1, demo2 = st.columns(2)
        with demo1:
            st.button("🟢 Load LOW demo", on_click=load_low_demo, use_container_width=True)
        with demo2:
            st.button("🔴 Load HIGH demo", on_click=load_high_demo, use_container_width=True)

        run = st.button("▶ RUN AI ANALYSIS", use_container_width=True)
        st.markdown('<div class="muted">Synthetic demo inputs only. No real employee data is used.</div>', unsafe_allow_html=True)

        if run:
            values = {
                "after_hours_logins": float(st.session_state.after_hours),
                "file_access_count": float(st.session_state.file_access),
                "email_activity": float(st.session_state.email_activity),
                "device_activity": float(st.session_state.device_activity),
                "web_activity": float(st.session_state.web_activity),
            }
            frame = pd.DataFrame([values], columns=FEATURES)
            rf_pred = int(rf_model.predict(frame)[0])
            rf_probs = rf_model.predict_proba(frame)[0]
            rf_p1 = float(rf_probs[list(rf_model.classes_).index(1)])
            pt_pred, pt_p1 = pytorch_predict(values)
            st.session_state.analysis_count += 1
            st.session_state.last_result = {
                "values": values,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rf_prediction": rf_pred,
                "rf_probability": rf_p1,
                "pt_prediction": pt_pred,
                "pt_probability": pt_p1,
            }

    with right:
        result = st.session_state.last_result
        if result is None:
            st.markdown(
                '<div class="result-mid"><div class="result-title">🟠 AWAITING ANALYSIS</div><div class="result-score">--</div><div class="result-meta">Choose Random Forest, PyTorch, or Compare Both, then run an analysis.</div></div>',
                unsafe_allow_html=True,
            )
        else:
            def result_card(title, prediction, p1):
                if p1 < 0.35:
                    css, icon, label = "result-low", "🟢", "LOWER-RISK DEMO SIGNAL"
                elif p1 <= 0.65:
                    css, icon, label = "result-mid", "🟠", "ELEVATED / UNCERTAIN DEMO SIGNAL"
                else:
                    css, icon, label = "result-high", "🔴", "HIGHER-RISK DEMO SIGNAL"
                st.markdown(
                    f'<div class="{css}"><div class="result-title">{icon} {label}</div><div class="result-score">{p1*100:.1f}%</div><div class="result-meta">{title} · CLASS-1 PROBABILITY · PREDICTED CLASS {prediction}</div></div>',
                    unsafe_allow_html=True,
                )

            selected = st.session_state.selected_model
            if selected == "🌲 Random Forest":
                result_card("🌲 Random Forest", result["rf_prediction"], result["rf_probability"])
            elif selected == "🧠 PyTorch Neural Network":
                result_card("🧠 PyTorch Neural Network", result["pt_prediction"], result["pt_probability"])
            else:
                c1, c2 = st.columns(2)
                with c1:
                    result_card("🌲 Random Forest", result["rf_prediction"], result["rf_probability"])
                with c2:
                    result_card("🧠 PyTorch Neural Network", result["pt_prediction"], result["pt_probability"])

            st.markdown('<div class="section-label">$ MODEL COMPARISON</div>', unsafe_allow_html=True)
            comp = pd.DataFrame(
                [
                    ["🌲 Random Forest", result["rf_prediction"], result["rf_probability"]],
                    ["🧠 PyTorch Neural Network", result["pt_prediction"], result["pt_probability"]],
                ],
                columns=["Model", "Predicted Class", "Class-1 Probability"],
            )
            comp["Class-1 Probability"] = comp["Class-1 Probability"].map(lambda x: f"{x*100:.1f}%")
            st.dataframe(comp, use_container_width=True, hide_index=True)

            st.markdown('<div class="section-label">$ INPUT VECTOR</div>', unsafe_allow_html=True)
            friendly = pd.DataFrame(
                [{
                    "🌙 After-hours": result["values"]["after_hours_logins"],
                    "📁 File access": result["values"]["file_access_count"],
                    "✉️ Email": result["values"]["email_activity"],
                    "💻 Device": result["values"]["device_activity"],
                    "🌐 Web": result["values"]["web_activity"],
                }]
            )
            st.dataframe(friendly, use_container_width=True, hide_index=True)

            st.markdown('<div class="section-label">$ RANDOM FOREST SIGNAL</div>', unsafe_allow_html=True)
            imp = pd.Series(
                rf_model.feature_importances_,
                index=["🌙 After-hours", "📁 File access", "✉️ Email", "💻 Device", "🌐 Web"],
            ).sort_values(ascending=False)
            st.bar_chart(imp, height=190)

            st.markdown(
                '<div class="warning-strip">⚠️ Educational prototype only. These outputs are demo classifications from two baseline models, not production security decisions or employee risk scores.</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="section-label">$ SYSTEM CONSOLE</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="terminal"><div><span class="term-green">[OK]</span> Behavioural vector validated</div><div><span class="term-green">[OK]</span> Random Forest inference completed</div><div><span class="term-blue">[OK]</span> PyTorch inference completed</div><div><span class="term-cyan">[DONE]</span> Analysis #{st.session_state.analysis_count} generated</div><div><span class="term-amber">[NOTE]</span> Synthetic demo mode</div></div>',
                unsafe_allow_html=True,
            )

# -----------------------------------------------------------------------------
# Alerts
# -----------------------------------------------------------------------------
elif page == "🚨 Alerts":
    st.markdown('<div class="section-label">$ ALERTS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card"><div class="card-title">🚨 DEMO ALERT STREAM</div><div class="muted">Synthetic classifications only - not a live SOC feed.</div></div>',
        unsafe_allow_html=True,
    )
    alerts = df.copy()
    alerts["severity"] = alerts[TARGET].map({0: "LOW", 1: "HIGH"})
    alerts["status"] = "DEMO"
    alerts["event_id"] = [f"DEMO-{i:03d}" for i in range(1, len(alerts) + 1)]
    st.dataframe(
        alerts[["event_id", "severity"] + FEATURES + [TARGET, "status"]],
        use_container_width=True,
        hide_index=True,
    )

# -----------------------------------------------------------------------------
# Model Lab
# -----------------------------------------------------------------------------
elif page == "🧠 Model Lab":
    st.markdown('<div class="section-label">$ MODEL LAB</div>', unsafe_allow_html=True)
    a, b, c, d = st.columns(4)
    vals = [
        ("🌲 Random Forest", "ONLINE"),
        ("🧠 PyTorch NN", "READY"),
        ("🧬 Features", str(len(FEATURES))),
        ("📊 Demo rows", str(len(df))),
    ]
    for col, (label, value) in zip([a, b, c, d], vals):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value metric-cyan">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-label">$ MODEL STACK</div>', unsafe_allow_html=True)
    x, y = st.columns(2)
    with x:
        st.markdown(
            '<div class="card"><div class="card-title">🌲 Random Forest</div><div class="muted">Scikit-learn supervised classification baseline.</div><br><b>100 decision trees</b></div>',
            unsafe_allow_html=True,
        )
    with y:
        st.markdown(
            '<div class="card"><div class="card-title">🧠 PyTorch Neural Network</div><div class="muted">Small feed-forward neural-network baseline.</div><br><b>5 → 16 → 8 → 2</b></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-label">$ RANDOM FOREST FEATURE IMPORTANCE</div>', unsafe_allow_html=True)
    imp = pd.Series(
        rf_model.feature_importances_,
        index=["🌙 After-hours", "📁 File access", "✉️ Email", "💻 Device", "🌐 Web"],
    ).sort_values(ascending=False)
    st.bar_chart(imp, height=230)

    st.markdown('<div class="section-label">$ SAME INPUT · TWO MODELS</div>', unsafe_allow_html=True)
    sample = {
        "after_hours_logins": 3.0,
        "file_access_count": 10.0,
        "email_activity": 12.0,
        "device_activity": 2.0,
        "web_activity": 15.0,
    }
    frame = pd.DataFrame([sample], columns=FEATURES)
    rf_pred = int(rf_model.predict(frame)[0])
    rf_p1 = float(rf_model.predict_proba(frame)[0][list(rf_model.classes_).index(1)])
    pt_pred, pt_p1 = pytorch_predict(sample)
    q = pd.DataFrame(
        [
            ["🌲 Random Forest", rf_pred, rf_p1],
            ["🧠 PyTorch Neural Network", pt_pred, pt_p1],
        ],
        columns=["Model", "Predicted Class", "Class-1 Probability"],
    )
    q["Class-1 Probability"] = q["Class-1 Probability"].map(lambda v: f"{v*100:.1f}%")
    st.dataframe(q, use_container_width=True, hide_index=True)
    st.markdown(
        '<div class="warning-strip">⚠️ Both models are learning baselines trained on the same synthetic demonstration dataset. Their probabilities are not real-world risk probabilities.</div>',
        unsafe_allow_html=True,
    )

    if st.button("♻️ Retrain Both Models", use_container_width=True):
        import subprocess
        result = subprocess.run([sys.executable, str(ROOT / "src" / "train_all.py")], capture_output=True, text=True)
        get_demo_metrics.clear()
        get_pytorch_model.clear()
        if result.returncode == 0:
            st.success("Random Forest + PyTorch models retrained successfully.")
            st.code(result.stdout)
        else:
            st.error("Retraining failed.")
            st.code(result.stderr or result.stdout)
        st.rerun()

# -----------------------------------------------------------------------------
# Dataset
# -----------------------------------------------------------------------------
elif page == "📊 Dataset":
    st.markdown('<div class="section-label">$ DATASET EXPLORER</div>', unsafe_allow_html=True)
    st.info("Synthetic demonstration dataset. Replace it with appropriately authorised research data before making research claims.")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('<div class="section-label">$ SUMMARY STATISTICS</div>', unsafe_allow_html=True)
    st.dataframe(df[FEATURES].describe().T, use_container_width=True)

# -----------------------------------------------------------------------------
# Terminal
# -----------------------------------------------------------------------------
elif page == "🖥️ Terminal":
    st.markdown('<div class="section-label">$ SYSTEM TERMINAL</div>', unsafe_allow_html=True)
    st.markdown(
        f'''<div class="terminal"><div><span class="term-cyan">insiderguard@ai</span>:~$ system status</div><div>RF MODEL.......... <span class="term-green">ONLINE</span></div><div>PYTORCH MODEL..... <span class="term-green">READY</span></div><div>FEATURES.......... {len(FEATURES)}</div><div>DATASET........... <span class="term-amber">SYNTHETIC DEMO</span></div><div>RF TEST ACCURACY.. {metrics['accuracy']*100:.1f}%</div><div>ANALYSES.......... {st.session_state.analysis_count}</div><div>MODE.............. EDUCATIONAL</div><br><div><span class="term-cyan">insiderguard@ai</span>:~$ note</div><div class="term-red">Do not use demo output as a production security decision.</div></div>''',
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------
elif page == "⚙️ Settings":
    st.markdown('<div class="section-label">$ SETTINGS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card"><div class="card-title">⚙️ SYSTEM CONFIGURATION</div><div class="muted">This learning build keeps external network access disabled.</div></div>',
        unsafe_allow_html=True,
    )
    st.checkbox("🖥️ Terminal-style logging", value=True, disabled=True)
    st.checkbox("🔐 Production mode", value=False, disabled=True)
    st.checkbox("🌐 External network access", value=False, disabled=True)
    st.caption("Production mode and external network access are intentionally disabled.")

st.markdown("---")
st.caption("🛡️ INSIDERGUARD AI • Educational research prototype • Random Forest + PyTorch")
