import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from model import OptimalVelocityModel
from pos_evol import plot_position_evolution
from stability import plot_stability
from single_vehicle import plot_vehicle_trajectory
from snapshot import plot_velocity_snapshot

import matplotlib
matplotlib.use("Qt5Agg")  # Use Qt5Agg backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- Global storage ---
model = None
figures = []
canvases = []

def clear_canvases():
    """Clear all existing plot canvases and ALL widgets in frame_plots"""
    for widget in frame_plots.winfo_children():
        widget.destroy()
    
    canvases.clear()
    figures.clear()
    # Close any matplotlib figures to free memory
    plt.close('all')
    
    # Show welcome message
    show_welcome_message()

def show_welcome_message():
    welcome_label = tk.Label(frame_plots, 
                            text="Welcome to the Optimal Velocity Model Simulator!\n\n"
                                 "Set your parameters above and click 'RUN SIMULATION' to generate plots.\n",
                            font=("Arial", 14), fg="gray", bg='white', justify='center')
    welcome_label.pack(pady=50)

def clear_plots():
    clear_canvases()


def run_simulation():
    # Remove ALL widgets including welcome message
    for widget in frame_plots.winfo_children():
        widget.destroy()
    clear_canvases()

    try:
        N = int(entry_N.get())
        L = float(entry_L.get())
        a = float(entry_a.get())
        t_total = float(entry_time.get())
        vehicle_num = int(entry_vehicle.get())
        snapshot_time = float(entry_snapshot.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        show_welcome_message()  # Show welcome message again if there's an error
        return

    if vehicle_num < 1 or vehicle_num > N:
        messagebox.showerror("Invalid vehicle number", f"Must be between 1 and {N}")
        show_welcome_message()  # Show welcome message again if there's an error
        return

    # Run model
    global model
    model = OptimalVelocityModel(N=N, L=L, a=a)
    model.run_simulation(t_total)

    # Generate and embed plots in the same window
    def embed_plot(fig, title):
        # Add title label
        label = tk.Label(frame_plots, text=title, font=("Arial", 14, "bold"), bg='white')
        label.pack(pady=(10, 5))
        
        # Create canvas and embed the figure
        canvas = FigureCanvasTkAgg(fig, master=frame_plots)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=5, padx=10, fill='both')
        
        # Store references
        canvases.append(canvas)
        figures.append((title.replace(" ", "_").lower() + ".png", fig))
        
        # Add separator line
        separator = tk.Frame(frame_plots, height=2, bg='lightgray')
        separator.pack(fill='x', pady=10, padx=20)

    # Generate plots and embed them
    try:
        # Create figures without showing them
        plt.ioff()
        
        fig1 = plot_position_evolution(model, return_fig=True)
        plt.close(fig1)  
        embed_plot(fig1, "Time Evolution of Vehicle Positions")

        fig2 = plot_stability(model, return_fig=True)
        plt.close(fig2)  
        embed_plot(fig2, "Stability Phase Diagram")

        fig3 = plot_vehicle_trajectory(model, vehicle_num, return_fig=True)
        plt.close(fig3)  
        embed_plot(fig3, f"Vehicle #{vehicle_num} Trajectory & Velocity")

        fig4 = plot_velocity_snapshot(model, snapshot_time, return_fig=True)
        plt.close(fig4)  
        embed_plot(fig4, f"System Snapshot at t={snapshot_time}")

        plt.ion()  
        
        canvas_container.yview_moveto(0)
        
        
    except Exception as e:
        plt.ion()
        messagebox.showerror("Simulation Error", f"Error during simulation: {str(e)}")
        show_welcome_message()

def save_all():
    if not figures:
        messagebox.showinfo("Nothing to save", "Please run the simulation first.")
        return
    
    saved_files = []
    for filename, fig in figures:
        try:
            fig.savefig(filename, bbox_inches='tight', dpi=300)
            saved_files.append(filename)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save {filename}: {str(e)}")
    
    if saved_files:
        messagebox.showinfo("Saved", f"Successfully saved {len(saved_files)} plots:\n" + 
                           "\n".join(saved_files))

root = tk.Tk()
root.title("Optimal Velocity Model Simulator")
root.state('zoomed')  
root.configure(bg='white')

# --- Top input panel ---
frame_input = tk.Frame(root, bg='lightblue', relief='raised', bd=2)
frame_input.pack(side=tk.TOP, fill='x', padx=5, pady=5)

# Input fields
input_frame = tk.Frame(frame_input, bg='lightblue')
input_frame.pack(pady=10)

row1 = tk.Frame(input_frame, bg='lightblue')
row1.pack(pady=2)

tk.Label(row1, text="N (vehicles):", bg='lightblue', font=('Arial', 10)).grid(row=0, column=0, padx=5, sticky='e')
entry_N = tk.Entry(row1, width=8, font=('Arial', 10))
entry_N.insert(0, "10")
entry_N.grid(row=0, column=1, padx=5)

tk.Label(row1, text="L (road length):", bg='lightblue', font=('Arial', 10)).grid(row=0, column=2, padx=5, sticky='e')
entry_L = tk.Entry(row1, width=8, font=('Arial', 10))
entry_L.insert(0, "20")
entry_L.grid(row=0, column=3, padx=5)

tk.Label(row1, text="a (sensitivity):", bg='lightblue', font=('Arial', 10)).grid(row=0, column=4, padx=5, sticky='e')
entry_a = tk.Entry(row1, width=8, font=('Arial', 10))
entry_a.insert(0, "1.0")
entry_a.grid(row=0, column=5, padx=5)

row2 = tk.Frame(input_frame, bg='lightblue')
row2.pack(pady=2)

tk.Label(row2, text="Total time:", bg='lightblue', font=('Arial', 10)).grid(row=0, column=0, padx=5, sticky='e')
entry_time = tk.Entry(row2, width=8, font=('Arial', 10))
entry_time.insert(0, "100.0")
entry_time.grid(row=0, column=1, padx=5)

tk.Label(row2, text="Vehicle # to track:", bg='lightblue', font=('Arial', 10)).grid(row=0, column=2, padx=5, sticky='e')
entry_vehicle = tk.Entry(row2, width=8, font=('Arial', 10))
entry_vehicle.insert(0, "1")
entry_vehicle.grid(row=0, column=3, padx=5)

tk.Label(row2, text="Snapshot time:", bg='lightblue', font=('Arial', 10)).grid(row=0, column=4, padx=5, sticky='e')
entry_snapshot = tk.Entry(row2, width=8, font=('Arial', 10))
entry_snapshot.insert(0, "50.0")
entry_snapshot.grid(row=0, column=5, padx=5)

# Buttons
buttons_frame = tk.Frame(input_frame, bg='lightblue')
buttons_frame.pack(pady=10)

btn_run = tk.Button(buttons_frame, text="RUN SIMULATION", command=run_simulation, 
                   bg="lightgreen", font=("Arial", 11, "bold"), width=14, height=1)
btn_run.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(buttons_frame, text="CLEAR PLOTS", command=clear_plots, 
                     bg="lightcoral", font=("Arial", 11, "bold"), width=14, height=1)
btn_clear.pack(side=tk.LEFT, padx=5)

btn_save = tk.Button(buttons_frame, text="SAVE ALL PLOTS", command=save_all, 
                    bg="lightyellow", font=("Arial", 11, "bold"), width=14, height=1)
btn_save.pack(side=tk.LEFT, padx=5)

# --- Main container for scrollable plots ---
main_container = tk.Frame(root)
main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Create scrollable area
canvas_container = tk.Canvas(main_container, bg='white')
scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas_container.yview)
scrollable_frame = tk.Frame(canvas_container, bg='white')

# Configure scrolling
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_container.configure(scrollregion=canvas_container.bbox("all"))
)

canvas_window = canvas_container.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_container.configure(yscrollcommand=scrollbar.set)

# Pack scrollable components
canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Frame for plots
frame_plots = scrollable_frame

# Bind mousewheel to canvas for scrolling
def _on_mousewheel(event):
    canvas_container.yview_scroll(int(-1*(event.delta/120)), "units")

canvas_container.bind("<MouseWheel>", _on_mousewheel)  # Windows
canvas_container.bind("<Button-4>", lambda e: canvas_container.yview_scroll(-1, "units"))  # Linux
canvas_container.bind("<Button-5>", lambda e: canvas_container.yview_scroll(1, "units"))   # Linux

# Make canvas expand to fill window width
def configure_canvas(event):
    canvas_width = event.width
    canvas_container.itemconfig(canvas_window, width=canvas_width)

canvas_container.bind('<Configure>', configure_canvas)

show_welcome_message()

if __name__ == "__main__":
    root.mainloop()