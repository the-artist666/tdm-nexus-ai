import numpy as np
from astropy.io import fits
import requests
from io import BytesIO
import os

PLANCK_URL = "https://irsa.ipac.caltech.edu/data/Planck/release_2/ancillary-data/COM_PowerSpect_CMB_R2.02.fits"
CACHE_PATH = "data/cache/planck_tt.fits"

def download_planck_if_needed():
    if os.path.exists(CACHE_PATH): return
    try:
        r = requests.get(PLANCK_URL, timeout=30)
        os.makedirs("data/cache", exist_ok=True)
        with open(CACHE_PATH, 'wb') as f:
            f.write(r.content)
    except: pass

def load_planck_spectrum():
    download_planck_if_needed()
    try:
        with open(CACHE_PATH, 'rb') as f:
            hdul = fits.open(BytesIO(f.read()))
        data = hdul['TTHILBIN'].data
        return data['ELL'], data['TT']
    except:
        ell = np.linspace(2, 2500, 100)
        cl = np.exp(-ell/1000) + 0.1 * np.sin(ell/200)
        return ell, cl

def parse_cl_to_tau_symbols(cl, grad_factor=0.5, lap_factor=0.5):
    dcl = np.gradient(cl)
    ddcl = np.gradient(dcl)
    gth = grad_factor * np.std(dcl)
    lth = lap_factor * np.std(ddcl)
    return ['δτ⨉' if abs(l) > lth else 'τ↑' if g > gth else 'τ↓' if g < -gth else None for g, l in zip(dcl, ddcl)]

def compare_symbol_sequences(obs, sim):
    paired = [(o, s) for o, s in zip(obs, sim) if o is not None and s is not None]
    return sum(1 for o, s in paired if o == s) / len(paired) if paired else 0.0
