import numpy as np
import matplotlib.pyplot as plt

def plot_stability(model, return_fig=False):
    """
    Plot phase diagram of stability and mark the current model parameters (a, b̄).
    """
    # Define V′(Δx) once
    dV = lambda x: 1 - np.tanh(x - 2)**2

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # ----- Left plot: V(Δx) and V′(Δx) -----
    b_vals = np.linspace(0.5, 5, 100)
    ax1.plot(b_vals, np.tanh(b_vals - 2) + np.tanh(2), 'b-', lw=2, label='V(Δx)')
    ax1.plot(b_vals, dV(b_vals), 'r-', lw=2, label="V′(Δx)")
    ax1.set_xlabel('Spacing Δx')
    ax1.set_ylabel('Value')
    ax1.set_title('Optimal Velocity and its Derivative')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # ----- Right plot: Stability phase diagram -----
    a_vals = np.linspace(0.1, 4, 100)
    b_grid = np.linspace(0.5, 4, 10000)
    B, A = np.meshgrid(b_grid, a_vals)
    stability = A > 2 * dV(B)

    ax2.contourf(B, A, stability, levels=[0, 0.5, 1], colors=['lightcoral', 'lightblue'], alpha=0.7)
    ax2.contour(B, A, stability.astype(int), levels=[0.5], colors='black', linewidths=2)

    ax2.set_xlabel('Spacing b̄')
    ax2.set_ylabel('Driver Sensitivity a')
    ax2.set_title('Stability Phase Diagram')
    ax2.grid(True, alpha=0.3)

    # Annotate stable/unstable zones
    ax2.text(3.5, 0.5, 'Unstable\n(Traffic Jams)', ha='center',
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    ax2.text(1, 3.5, 'Stable\n(Free Flow)', ha='center',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    # ----- Mark current parameters -----
    current_a = model.a
    current_b = model.L / model.N
    ax2.plot(current_b, current_a, 'ro', markersize=10, markeredgecolor='black', label='Current Params')

    # Status label
    stable = current_a > 2 * dV(current_b)
    status = 'Stable' if stable else 'Unstable'
    color = 'blue' if stable else 'red'
    ax2.text(current_b + 0.1, current_a, status, fontsize=10, color=color,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8), va='center')

    ax2.legend()
    plt.tight_layout()
    if return_fig:
        return fig
