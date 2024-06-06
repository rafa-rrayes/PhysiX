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

p1 = Point([5, 0, 0], [0, 2, 0], [0, 0, 0], 1)
p2 = Point([0, 0, 0], [0, 0, 0], [0, 0, 0], 40)

p1.f = f
p2.f = f
world = World([p1, p2])
time_points = np.arange(0, 50, 0.01)
world.calculate(time_points)
world.animate()