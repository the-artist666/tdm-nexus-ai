import streamlit as st
import numpy as np
import plotly.express as px
from core.tdm_simulator import simulate_tdm_field_4d
from core.tdm_parser import parse_tau_field
from core.cosmology_matcher import load_planck_spectrum, parse_cl_to_tau_symbols, compare_symbol_sequences
from core.nasa.apod import fetch_apod
from core.nasa.mars import fetch_mars_photo
from core.nasa.epic import fetch_epic_image
from core.nasa.neo import fetch_neo_count
from core.nasa.exoplanets import fetch_exoplanet_count

st.set_page_config(page_title="TDM Nexus AI v9.0", layout="wide", page_icon="🌌")

# --- STYLING ---
st.markdown("""
<style>
    .main { background-color: #0a0a0a; color: #00ff88; }
    h1, h2 { color: #00ccff; text-shadow: 0 0 10px rgba(0, 204, 255, 0.5); }
    .stButton>button { background-color: #00ccff; color: black; font-weight: bold; }
    .metric { font-size: 24px; color: #00ff88; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🌌 TDM Nexus AI v9.0")
st.subheader("Validating TDM 4.0 with Real NASA APIs Only")

# --- FIX: Add fallback for NASA API key ---
try:
    api_key = st.secrets["NASA_API_KEY"]
except KeyError:
    st.warning("NASA API key not found. Using DEMO_KEY (limited). Add your key in Streamlit Secrets.")
    api_key = "DEMO_KEY"  # Safe for testing

with st.sidebar:
    st.image("https://api.nasa.gov/images/logo.png", width=120)
    st.header("🔧 Controls")
    mass = st.slider("TDM Field Mass", 0.01, 0.5, 0.1)
    lambda_ = st.slider("Self-Coupling λ", 0.01, 0.2, 0.05)
    run_sim = st.button("🚀 Run TDM Simulation")

if run_sim:
    with st.spinner("Simulating 4D TDM Field..."):
        tau_4d = simulate_tdm_field_4d(mass=mass, lambda_=lambda_)
        tau_1d = tau_4d[:, 7, 7, 7]
        sim_symbols = parse_tau_field(tau_1d)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. TDM Field Evolution")
        st.line_chart(tau_1d)
        st.markdown(f"<div class='metric'>Fluctuation: {np.std(tau_1d):.2e}</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("2. τ-Language Symbols")
        st.code(" ".join([s or "·" for s in sim_symbols[:60]]))

    st.markdown("---")
    st.subheader("3. Match with Planck CMB")
    ell, cl = load_planck_spectrum()
    obs_symbols = parse_cl_to_tau_symbols(cl)
    match_score = compare_symbol_sequences(obs_symbols, sim_symbols)
    st.progress(match_score)
    st.markdown(f"<div class='metric'>✅ Match Score: {match_score:.2%}</div>", unsafe_allow_html=True)

    fig = px.scatter(x=ell[:len(obs_symbols)], y=[1]*len(obs_symbols), color=obs_symbols,
                     color_discrete_map={'τ↑':'green','τ↓':'red','δτ⨉':'blue',None:'gray'},
                     title="CMB Symbolic Pattern")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("4. Real NASA Mission Data")

    a, m, e, n = st.columns(4)
    with a: st.image(fetch_apod(api_key)["url"], caption="APOD")
    with m: st.image(fetch_mars_photo(api_key), caption="Mars")
    with e: st.image(fetch_epic_image(api_key), caption="Earth (EPIC)")
    with n: st.metric("NEOs Today", fetch_neo_count(api_key))

    st.markdown(f"🪐 **Exoplanets**: {fetch_exoplanet_count()}")
else:
    st.info("👈 Adjust parameters and click 'Run Simulation'")

st.markdown('<div style="text-align:center; margin-top:50px; color:#aaa;">TDM Nexus AI v9.0 | Dr. Adnane Lahguidi | Based on TDM 4.0 Theory</div>', unsafe_allow_html=True)
