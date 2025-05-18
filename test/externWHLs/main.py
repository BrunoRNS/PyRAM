import numpy as np # type: ignore

import matplotlib.pyplot as plt # type: ignore

class DataGenerator:
    def __init__(self, n_points=100):
        self.n_points = n_points

    def sine_wave(self, freq=1.0, amp=1.0):
        x = np.linspace(0, 2 * np.pi, self.n_points)
        y = amp * np.sin(freq * x)
        return x, y

    def cosine_wave(self, freq=1.0, amp=1.0):
        x = np.linspace(0, 2 * np.pi, self.n_points)
        y = amp * np.cos(freq * x)
        return x, y

    def random_data(self):
        x = np.linspace(0, 10, self.n_points)
        y = np.random.rand(self.n_points)
        return x, y

class Plotter:
    def __init__(self, title="Plot"):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(title)

    def plot(self, x, y, label=None, style='-'):
        self.ax.plot(x, y, style, label=label)

    def scatter(self, x, y, label=None, color='r'):
        self.ax.scatter(x, y, label=label, color=color)

    def show(self):
        self.ax.legend()
        plt.show()

class MultiPlotter:
    def __init__(self, nrows=1, ncols=2, figsize=(10, 4)):
        self.fig, self.axes = plt.subplots(nrows, ncols, figsize=figsize)

    def plot_on(self, idx, x, y, label=None, style='-'):
        ax = self.axes[idx]
        ax.plot(x, y, style, label=label)
        ax.legend()

    def set_title(self, idx, title):
        self.axes[idx].set_title(title)

    def show(self):
        plt.tight_layout()
        plt.show()

def main():
    gen = DataGenerator(n_points=200)
    x1, y1 = gen.sine_wave(freq=2, amp=1)
    x2, y2 = gen.cosine_wave(freq=2, amp=0.5)
    x3, y3 = gen.random_data()

    # Single plot
    plotter = Plotter(title="Sine and Cosine Waves")
    plotter.plot(x1, y1, label="Sine (2Hz)", style='b-')
    plotter.plot(x2, y2, label="Cosine (2Hz, 0.5x)", style='g--')
    plotter.scatter(x3, y3, label="Random Data", color='r')
    plotter.show()

    # Multiple subplots
    multi = MultiPlotter(nrows=1, ncols=2)
    multi.plot_on(0, x1, y1, label="Sine", style='b-')
    multi.set_title(0, "Sine Wave")
    multi.plot_on(1, x2, y2, label="Cosine", style='g--')
    multi.set_title(1, "Cosine Wave")
    multi.show()

if __name__ == "__main__":
    main()