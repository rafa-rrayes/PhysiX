import numpy as np
from world import World, Point

def f(t, self, objects):
    force = np.array([0, 0, 5], dtype=float)
    Fel = 10 * (self.position - objects[0].position)
    Fel += 10 * (self.position - objects[1].position)
    Far =  0.3*self.velocity**2 * np.sign(self.velocity)
    force += - Fel - Far
    return force
def f_ponta(t, self, objects):
    force = np.array([0, 0, 5], dtype=float)
    if 3 < t <3.1:
        force += np.array([0, -400, 0], dtype=float)
    Fel = 10 * (self.position - objects[1].position)
    Far =  0.3*self.velocity**2 * np.sign(self.velocity)
    force += - Fel - Far
    return force
p0 = Point([0, 0, 0], [0, 0, 0], name = 'fixed')
p1 = Point([1, 0, -1], [0, 0, 0], mass=0.5, name='first')
p2 = Point([2, 0, -1], [0, 0, 0],mass=1, name = 'second')


p1.f = f
p2.f = f_ponta

world = World([p0, p1, p2])

time_points = np.arange(0, 40, 0.01)

results = world.calculate(time_points)

world.animate()