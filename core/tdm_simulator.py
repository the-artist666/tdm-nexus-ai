import numpy as np

def simulate_tdm_field_4d(T=30, X=15, Y=15, Z=15, mass=0.1, lambda_=0.05, alpha=0.1, beta=0.05):
    tau = np.zeros((T, X, Y, Z))
    tau[0] = np.random.normal(0, 1e-3, (X, Y, Z))
    dt, dx = 1e-3, 1e-3

    def dAlembertian(tau_grid, t, x, y, z):
        if t < 1 or t >= T-1: return 0
        d2t = (tau_grid[t+1,x,y,z] - 2*tau_grid[t,x,y,z] + tau_grid[t-1,x,y,z]) / dt**2
        d2x = (tau_grid[t,x+1,y,z] - 2*tau_grid[t,x,y,z] + tau_grid[t,x-1,y,z]) / dx**2 if 0 < x < X-1 else 0
        d2y = (tau_grid[t,x,y+1,z] - 2*tau_grid[t,x,y,z] + tau_grid[t,x,y-1,z]) / dx**2 if 0 < y < Y-1 else 0
        d2z = (tau_grid[t,x,y,z+1] - 2*tau_grid[t,x,y,z] + tau_grid[t,x,y,z-1]) / dx**2 if 0 < z < Z-1 else 0
        return d2t - (d2x + d2y + d2z)

    def potential_derivative(tau_val):
        return 4 * lambda_ * tau_val**3 - 2 * mass * tau_val

    for t in range(1, T-1):
        for x in range(1, X-1):
            for y in range(1, Y-1):
                for z in range(1, Z-1):
                    box_tau = dAlembertian(tau, t, x, y, z)
                    V_prime = potential_derivative(tau[t, x, y, z])
                    tau[t+1, x, y, z] = tau[t, x, y, z] + alpha * box_tau - beta * V_prime
    return tau
