import numpy as np
import matplotlib.pyplot as plt 
def unwrap_positions(pos_array, time_array, L):
    """
    Unwrap vehicle positions to prevent wrap-around plotting artifacts.
    Inserts NaNs where vehicle wraps around the ring.
    """
    N = pos_array.shape[1]
    Tmax = len(time_array)
    unwrapped = []
    
    for n in range(N):
        x_vals = pos_array[:, n]  # positions for vehicle n
        x_plot = [x_vals[0]]  # start with first position
        t_plot = [time_array[0]]  # start with first time
        
        for i in range(1, Tmax):
            dx = x_vals[i] - x_vals[i - 1]
            if dx < -L / 2:  # wrapped from L to 0
                x_plot.append(np.nan)
                t_plot.append(np.nan)
            elif dx > L / 2:  # wrapped from 0 to L
                x_plot.append(np.nan)
                t_plot.append(np.nan)
            
            x_plot.append(x_vals[i])
            t_plot.append(time_array[i])
            
        unwrapped.append((np.array(t_plot), np.array(x_plot)))
    return unwrapped

def plot_position_evolution(model, title_suffix="", return_fig=False):
    """Plot time evolution of vehicle positions (unwrapped to remove periodic jumps)."""
    time, x_hist, _ = model.get_trajectories()

    fig, ax = plt.subplots(figsize=(12, 8))

    colors = plt.cm.tab10(np.linspace(0, 1, model.N))

    unwrapped_data = unwrap_positions(x_hist, time, model.L)

    for i, (t_plot, x_plot) in enumerate(unwrapped_data):
        ax.plot(t_plot, x_plot, color=colors[i], linewidth=1.5, label=f'Vehicle {i+1}')

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Position', fontsize=12)
    ax.set_title(f'Time Evolution of Vehicle Positions{title_suffix}', fontsize=14)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    if return_fig:
        return fig
