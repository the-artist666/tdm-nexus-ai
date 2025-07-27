import numpy as np

def parse_tau_field(tau_array, threshold=1e-5):
    symbols = []
    dtau = np.gradient(tau_array)
    ddtau = np.gradient(dtau)
    for g, l in zip(dtau, ddtau):
        if abs(l) > threshold * 10:
            symbols.append('δτ⨉')
        elif g > threshold:
            symbols.append('τ↑')
        elif g < -threshold:
            symbols.append('τ↓')
        else:
            symbols.append(None)
    return symbols
