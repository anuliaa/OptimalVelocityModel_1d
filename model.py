import numpy as np

class OptimalVelocityModel:
    def __init__(self, N, L, a, dt=0.01):

        """
        Initialize the Optimal Velocity Model
        
        Parameters:
        N: Number of vehicles
        L: Length of the road (periodic boundary)
        a: Driver sensitivity parameter
        dt: Time step for integration
        """
        self.N = N
        self.L = L
        self.a = a
        self.dt = dt
        
        # Initialize positions and velocities
        self.reset_simulation()
        
    def reset_simulation(self):
        """Reset the simulation with uniform initial conditions plus small perturbations"""
        self.x = (np.linspace(0, self.L, self.N, endpoint=False) + np.random.uniform(-0.01, 0.01, self.N)) % self.L
        
        # Initial velocities: optimal velocity for uniform spacing
        uniform_spacing = self.L / self.N
        self.v = np.full(self.N, self.optimal_velocity(uniform_spacing))
        
        # Storage for trajectories
        self.x_history = [self.x.copy()]
        self.v_history = [self.v.copy()]
        self.time_history = [0.0]
        
    def optimal_velocity(self, delta_x):
        return np.tanh(delta_x - 2) + np.tanh(2)
    
    
    def get_spacing(self):
        """Calculate spacing between consecutive vehicles (with periodic boundary)"""
        spacing = np.zeros(self.N)
        spacing = (np.roll(self.x, -1) - self.x) % self.L % self.L
        return spacing
    
    def update(self):
        """Update positions and velocities for one time step using Euler method"""
        spacing = self.get_spacing()
        
        # acceleration: a[V(Δx) - v]
        acceleration = self.a * (self.optimal_velocity(spacing) - self.v)
        
        # Update velocities and positions
        self.v += acceleration * self.dt
        self.x = (self.x + self.v * self.dt) % self.L
        
        # Store history
        self.x_history.append(self.x.copy())
        self.v_history.append(self.v.copy())
        self.time_history.append(self.time_history[-1] + self.dt)
    
    def run_simulation(self, total_time):
        """Run the simulation for a given total time"""
        steps = int(total_time / self.dt)
        
        for _ in range(steps):
            self.update()
    
    def get_trajectories(self):
        """Return trajectories as numpy arrays"""
        return np.array(self.time_history), np.array(self.x_history), np.array(self.v_history)

