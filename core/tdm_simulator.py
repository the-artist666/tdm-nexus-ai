import numpy as np

def simulate_tdm_field_4d(T=30, X=15, Y=15, Z=15, mass=0.1, lambda_=0.05, alpha=0.01, beta=0.01):
    """
    Simulates the TDM 4.0 scalar field in 4D Minkowski spacetime.
    
    Solves: □τ = -m²τ - λτ³
    Using: τ_{t+1} = τ_t + α□τ - β ∂V/∂τ
    
    Parameters:
    - T, X, Y, Z: Grid dimensions (time, space)
    - mass: TDM field mass (m_τ)
    - lambda_: Self-coupling strength (λ)
    - alpha: d'Alembertian update weight
    - beta: Potential force weight
    
    Returns:
    - 4D numpy array of τ-field values
    """
    # Initialize 4D field with small quantum fluctuations
    tau = np.zeros((T, X, Y, Z))
    tau[0] = np.random.normal(0, 1e-4, (X, Y, Z))  # Small initial fluctuation

    # Spacetime step sizes
    dt = 1e-3
    dx = 1e-2  # Larger dx for stability

    def dAlembertian(tau_grid, t, x, y, z):
        """Compute □τ = ∂²τ/∂t² - ∇²τ (d'Alembert operator)"""
        if t < 1 or t >= T - 1:
            return 0.0
        
        # Time derivative: ∂²τ/∂t²
        d2t = (tau_grid[t+1, x, y, z] - 2*tau_grid[t, x, y, z] + tau_grid[t-1, x, y, z]) / (dt**2)
        
        # Spatial derivatives: ∇²τ
        d2x = 0.0
        if 0 < x < X - 1:
            d2x = (tau_grid[t, x+1, y, z] - 2*tau_grid[t, x, y, z] + tau_grid[t, x-1, y, z]) / (dx**2)
        
        d2y = 0.0
        if 0 < y < Y - 1:
            d2y = (tau_grid[t, x, y+1, z] - 2*tau_grid[t, x, y, z] + tau_grid[t, x, y-1, z]) / (dx**2)
        
        d2z = 0.0
        if 0 < z < Z - 1:
            d2z = (tau_grid[t, x, y, z+1] - 2*tau_grid[t, x, y, z] + tau_grid[t, x, y, z-1]) / (dx**2)
        
        # Return □τ = ∂²τ/∂t² - (∂²τ/∂x² + ∂²τ/∂y² + ∂²τ/∂z²)
        return d2t - (d2x + d2y + d2z)

    def potential_derivative(tau_val):
        """Compute ∂V/∂τ = m²τ + λτ³"""
        # Clamp tau to prevent overflow in τ³
        tau_val = np.clip(tau_val, -1.0, 1.0)
        return 4 * lambda_ * tau_val**3 - 2 * mass * tau_val

    # Main simulation loop
    for t in range(1, T - 1):
        for x in range(1, X - 1):
            for y in range(1, Y - 1):
                for z in range(1, Z - 1):
                    # Compute d'Alembertian
                    box_tau = dAlembertian(tau, t, x, y, z)
                    
                    # Compute potential force
                    V_prime = potential_derivative(tau[t, x, y, z])
                    
                    # Update rule with small coefficients for stability
                    new_tau = tau[t, x, y, z] + alpha * box_tau - beta * V_prime
                    
                    # Clamp the field value to prevent blowup
                    tau[t+1, x, y, z] = np.clip(new_tau, -10.0, 10.0)
    
    return tau
