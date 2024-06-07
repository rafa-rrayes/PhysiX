import numpy as np

def nth_prime(n):
    primes = [2]
    num = 3
    while len(primes) < n:
        for prime in primes:
            if num % prime == 0:
                break
        else:
            primes.append(num)
        num += 2
    return primes[-1]
global _gravitated_objects
_gravitated_objects = {}
def gravity(self, objects, g=1):
    global _gravitated_objects
    total_force = np.array([0.0, 0.0, 0.0])
    for object in objects:
        if f"{object.id*self.id}" in _gravitated_objects:
            total_force -= _gravitated_objects[f"{object.id*self.id}"]
            continue
        distance = np.linalg.norm(object.position - self.position)
        if distance > 0:  # To avoid division by zero
            vector = object.position - self.position
            force_magnitude =  g*(self.mass*object.mass) / distance**2
            gravityF = force_magnitude * (vector / distance)
            _gravitated_objects[f"{object.id*self.id}"] = gravityF
            total_force += gravityF
    return total_force
class World:
    def __init__(self, objects):
        self.objects = objects
        for i, object in enumerate(self.objects):
            object.id = nth_prime(i+1)
    
    
    def calculate(self, t):
        global _gravitated_objects
        for object in self.objects:
            object.start(t)
        dt = t[1] - t[0]
        self.dt = dt
        for i in range(1, len(t)):
            _gravitated_objects = {}
            for num, object in enumerate(self.objects):
                previous_position = object.results[i-1][0]
                previous_velocity = object.results[i-1][1]
                previous_acceleration = object.results[i-1][2]

                # Calculate new position using Verlet integration
                new_position = previous_position + previous_velocity * dt + 0.5 * previous_acceleration * dt**2

                # Compute the force and new acceleration at the new position
                new_force = np.array(object.f(t[i], object, self.objects[0:num] + self.objects[num+1:]))
                new_acceleration = new_force / object.mass

                # Calculate new velocity using Verlet integration
                new_velocity = previous_velocity + 0.5 * (previous_acceleration + new_acceleration) * dt

                # Update results
                object.results[i] = np.array([new_position, new_velocity, new_acceleration])
            for object in self.objects:
                object.position = object.results[i][0]
                object.velocity = object.results[i][1]
                object.acceleration = object.results[i][2]
        return np.array([object.results for object in self.objects])
    def animate(self):
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        lines = []
        for object in self.objects:
            line, = ax.plot([], [], [], label=object.name, color=object.color, marker='o', markersize=object.size)
            lines.append(line)
        def init():
            ax.set_xlim([2, -2])
            ax.set_ylim([2, -2])
            ax.set_zlim([2, -2])
            for line in lines:
                line.set_data([], [])
                line.set_3d_properties([])
            return lines

        def update(frame):
            for line, object in zip(lines, self.objects):
                if not object.trail:
                    line.set_data([],[])
                    line.set_3d_properties([])
                    xdata = [res[0][0] for res in object.results[frame:frame+1]]
                    ydata = [res[0][1] for res in object.results[frame:frame+1]]
                    zdata = [res[0][2] for res in object.results[frame:frame+1]]
                    line.set_data(xdata, ydata)
                    line.set_3d_properties(zdata)
                else:
                    xdata = [res[0][0] for res in object.results[:frame+1]]
                    ydata = [res[0][1] for res in object.results[:frame+1]]
                    zdata = [res[0][2] for res in object.results[:frame+1]]
                    line.set_data(xdata, ydata)
                    line.set_3d_properties(zdata)
            return lines
        ani = animation.FuncAnimation(fig, update, frames=len(self.objects[0].results),interval=1000*self.dt, init_func=init, blit=True)
        plt.legend()
        plt.show()
        return ani

    




class Point:
    def __init__(self,position, velocity=0, mass=1,**kargs):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.acceleration = np.zeros(3)
        self.name = kargs.get('name')
        self.color = kargs.get('color')
        self.trail = kargs.get('trail', False)
        self.size = kargs.get('size', 3)
    def start(self, t):
        self.results = np.zeros((len(t), 3, 3))
        self.results[0] = np.array([self.position, self.velocity, self.acceleration])
    def f(self, t, y, objects):
        return np.array([0, 0, 0])
