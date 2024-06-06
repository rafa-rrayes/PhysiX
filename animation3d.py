import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
from world import World, Point

# Example data
def f(t,self, objects):
    
    #gravitate objects
    gravityF = np.array([0.0, 0.0, 0.0])
    for object in objects:
        distance = np.linalg.norm(object.position - self.position)
        if distance > 0:  # To avoid division by zero
            vector = object.position - self.position
            force_magnitude =  (self.mass*object.mass) / distance**2
            gravityF += force_magnitude * (vector / distance)
    return gravityF

p1 = Point([2, 0, 1], [0, 1, 0], [0, 0, 0], 2)
p2 = Point([0, 0, 0], [0, 0, 0], [0, 0, 0], 4)

p1.f = f
# p2.f = f
world = World([p1, p2])
time_points = np.arange(0, 50, 0.01)
world.calculate(time_points)
world.animate()
# Initialize the figure and 3D axis
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot the initial positions


# # Set the axis limits
# ax.set_xlim(-5, 5)
# ax.set_ylim(-5, 5)
# ax.set_zlim(-5, 5)


# # Update function for the animation
# print(p1.results[:10])
# x1 = p1.results[:,0,0]
# y1 = p1.results[:,0,1]
# z1 = p1.results[:,0,2]
# x2 = p2.results[:,0,0]
# y2 = p2.results[:,0,1]
# z2 = p2.results[:,0,2]

# line1, = ax.plot(x1, y1, z1, 'ro', label='Point 1')
# line2, = ax.plot(x2, y2, z2,'bo', label='Point 2')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.legend()

# # Update function for the animation
# def update(num, x1, y1, z1, x2, y2, z2, line1, line2):
#     line1.set_data([], [])
#     line1.set_3d_properties([])
#     line2.set_data([], [])
#     line2.set_3d_properties([])

#     # Set current frame's position
#     line1.set_data(x1[num:num+1], y1[num:num+1])
#     line1.set_3d_properties(z1[num:num+1])
#     line2.set_data(x2[num:num+1], y2[num:num+1])
#     line2.set_3d_properties(z2[num:num+1])
#     # print(x1[num], y1[num], z1[num])
#     return line1, line2

# # Create the animation
# ani = animation.FuncAnimation(fig, update, frames=len(time_points), fargs=(x1, y1, z1, x2, y2, z2, line1, line2), interval=10, blit=True)

# # Show the plot
# plt.show()
