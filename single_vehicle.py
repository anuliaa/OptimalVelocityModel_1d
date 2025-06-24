import matplotlib.pyplot as plt

def plot_vehicle_trajectory(model, vehicle_num, return_fig=False):
    """Plot trajectory and velocity evolution for a specific vehicle"""
    if vehicle_num < 1 or vehicle_num > model.N:
        print(f"Error: Vehicle number must be between 1 and {model.N}")
        return
    
    vehicle_idx = vehicle_num - 1  # Convert to 0-based indexing
    time, x_hist, v_hist = model.get_trajectories()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Position evolution
    ax1.plot(time, x_hist[:, vehicle_idx], 'b-', linewidth=2)
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Position', fontsize=12)
    ax1.set_title(f'Position Evolution of Vehicle #{vehicle_num}', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Velocity evolution
    ax2.plot(time, v_hist[:, vehicle_idx], 'r-', linewidth=2)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Velocity', fontsize=12)
    ax2.set_title(f'Velocity Evolution of Vehicle #{vehicle_num}', fontsize=14)
    ax2.grid(True, alpha=0.3)
        
    plt.tight_layout()
    if return_fig:
        return fig