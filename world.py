import numpy as np
class World:
    def __init__(self, objects):
        self.objects = objects
    def calculate(self, t):
        for object in self.objects:
            object.start(t)
        dt = t[1] - t[0]
        self.dt = dt
        for i in range(1, len(t)):

            for num, object in enumerate(self.objects):
                force = object.f(t[i-1], object, self.objects[0:num] + self.objects[num+1:])
                position = object.results[i-1][0] + dt * object.results[i-1][1]
                velocity = object.results[i-1][1] + dt * object.results[i-1][2]
                acceleration = force / object.mass
                object.results[i] = np.array([position, velocity, acceleration])
            for object in self.objects:
                object.position = object.results[i][0]
                object.velocity = object.results[i][1]
                object.acceleration = object.results[i][2]
        return object.results
    def animate(self):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.animation as animation
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        lines = []
        for object in self.objects:
            line, = ax.plot([], [], [], label=object.name, color=object.color, marker='o')
            lines.append(line)
        def init():
            ax.set_xlim([10, -10])
            ax.set_ylim([10, -10])
            ax.set_zlim([10, -10])
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
    def __init__(self,position, velocity, acceleration, mass,**kargs):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.acceleration = np.array(acceleration)
        self.name = kargs.get('name')
        self.color = kargs.get('color')
        self.trail = kargs.get('trail', False)
        

    def start(self, t):
        self.results = np.zeros((len(t), 3, 3))
        self.results[0] = np.array([self.position, self.velocity, self.acceleration])
    def f(self, t, y, objects):
        return np.array([0, 0, 0])


if __name__ == '__main__':
    import time
    def f(t, y, objects):
        position, velocity, acceleration = y
        #gravitate objects
        for object in objects:
            distance = np.abs(object.position - position)
            gravityF = 1 / distance**2

        return gravityF

    p1 = Point(1, [1, 1, 1], [0, 0, 0], [0, 0, 0])
    p2 = Point(1, [0, 0, 0], [0, 0, 0], [0, 0, 0])

    p1.f = f
    p2.f = f
    world = World([p1, p2])
    t = np.arange(0, 10, 0.01)
    start = time()
    world.calculate(t)
    print(time() - start)
    # make a 3 animation of the two points
