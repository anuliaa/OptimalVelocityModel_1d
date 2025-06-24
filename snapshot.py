import numpy as np
import matplotlib.pyplot as plt

def plot_velocity_snapshot(model, snapshot_time, return_fig=False):
    """Plot clean line plots showing system state at a specific time"""
    time, x_hist, v_hist = model.get_trajectories()
    
    # Find the closest time index
    time_idx = np.argmin(np.abs(np.array(time) - snapshot_time))
    actual_time = time[time_idx]
    
    # Get positions and velocities at this time
    positions = x_hist[time_idx, :]
    velocities = v_hist[time_idx, :]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Top plot: Position vs Car Number (shows spatial distribution)
    vehicle_numbers = np.arange(1, model.N + 1)
    ax1.plot(vehicle_numbers, positions, 'bo-', linewidth=2, 
             markersize=4, markerfacecolor='lightblue', markeredgecolor='blue')
    
    ax1.set_xlabel('Vehicle Number', fontsize=12)
    ax1.set_ylabel('Position along road', fontsize=12)
    ax1.set_title(f'Vehicle Positions at t = {actual_time:.2f}', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1, model.N)
    ax1.set_ylim(0, model.L)
    
    # Add some position statistics
    pos_stats_text = f'Pos Range: [{np.min(positions):.1f}, {np.max(positions):.1f}]'
    ax1.text(0.98, 0.02, pos_stats_text, transform=ax1.transAxes, 
             verticalalignment='bottom', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8),
             fontsize=10)
    
    # Bottom plot: Velocity profile as continuous line
    ax2.plot(vehicle_numbers, velocities, 'r-', linewidth=2, marker='o', 
             markersize=4, markerfacecolor='lightcoral', markeredgecolor='red')
    
    ax2.set_xlabel('Vehicle Number', fontsize=12)
    ax2.set_ylabel('Velocity', fontsize=12)
    ax2.set_title(f'Velocity Profile at t = {actual_time:.2f}', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(1, model.N)

    plt.tight_layout()
    if return_fig:
        return fig