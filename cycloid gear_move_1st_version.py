import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
R = 59 #pin pitch circle radius(=P.C.D/2)
R_r = 2.5 #pin radius
E = 1.1 #eccentricity
N = 40 #Number of pins
μ = R / (E * N) #Trochoid ratio #To create a curve that does not twist, it must be greater than 1, and in Japan, a correction factor x is used.
σ_t = float(input("Input Tooth tolerance : ")) #Tooth tolerance

# Set angle range to radians (np.linspace 사용)
angles = np.linspace(0, 2 * np.pi, 10000)

# Initial location settings
start_point = [[E, 0], [0, E], [-E, 0], [0, -E]]
start_point_x = start_point[N % 4][0]
start_point_y = start_point[N % 4][1]

fig, ax = plt.subplots()
ax.set_aspect(1)
ax.set_xlim(-2*R - E - 1, 2*R + E + 1)
ax.set_ylim(-2*R - E - 1, 2*R + E + 1)
ax.add_artist(plt.Circle((0, 0), R, fill=False))
# Drawing pins
for i in range(N):
    theta = 360 / (N) * i
    x, y = -np.sin(np.radians(theta)) * R, np.cos(np.radians(theta)) * R
    ax.add_artist(plt.Circle((x, y), R_r, fill=False))

# Trajectory initialization
path, = ax.plot([], [], 'b-', linewidth=0.5)

# animation update function
def update(frame):
    θ = np.radians(frame)
    x_coords = []
    y_coords = []

    for Φ in angles: #Speed Ratio n-1/1 -> (N - 1) * -θ / θ
        ψ = -np.arctan2(np.sin((N - 1) * Φ), (μ - np.cos((N - 1) * Φ)))
        x = R * np.cos(Φ) - (R_r+σ_t) * np.cos(Φ + ψ) - E * np.cos(N * Φ)
        y = R * np.sin(Φ) - (R_r+σ_t) * np.sin(Φ + ψ) - E * np.sin(N * Φ)
        x_coords.append(x * np.cos(θ) - y * np.sin(θ) + start_point_x * np.cos((N - 1) * -θ) - start_point_y * np.sin((N - 1) * -θ))
        y_coords.append(x * np.sin(θ) + y * np.cos(θ) + start_point_x * np.sin((N - 1) * -θ) + start_point_y * np.cos((N - 1) * -θ))

    path.set_data(x_coords, y_coords)
    return path,

ani = animation.FuncAnimation(fig, update, frames=range(0, 3600, 1), blit=True)

plt.title('RV reducer')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.axis('equal')
plt.grid(True)
plt.show()



