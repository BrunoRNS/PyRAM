"""
This script demonstrates custom data generation and plotting utilities using NumPy and Matplotlib.
Modules and Classes:
--------------------
- DataGenerator: Generates sine, cosine, and random data for plotting.
- Plotter: Provides a simple interface for plotting and displaying single plots.
- MultiPlotter: Facilitates plotting on multiple subplots within a single figure.
Functions:
- test_DataGenerator_sine_wave(): Tests the sine_wave method of DataGenerator for correct output.
- test_DataGenerator_cosine_wave(): Tests the cosine_wave method of DataGenerator for correct output.
- test_DataGenerator_random_data(): Tests the random_data method of DataGenerator for correct output.
- test_Plotter_methods(monkeypatch): Tests Plotter methods using monkeypatching for correct plotting calls.
- test_MultiPlotter_methods(monkeypatch): Tests MultiPlotter methods using monkeypatching for correct plotting calls.
- test_main_runs(monkeypatch): Tests that the main() function runs without displaying plots.
- main(): Generates example data and demonstrates usage of Plotter and MultiPlotter.
Usage:
------
- The script can be run directly to visualize example sine, cosine, and random data using both single and multiple plots.
- The test functions provide basic unit tests for the data generation and plotting classes.
Notes:
------
- NumPy and Matplotlib are required.
- The script is designed to work in environments where libraries may be installed in custom directories.
We have to use in this way because we're creating a directory speccially for matplotlib and numpy.

Running a command based on this you will have to use the same import style:

- pyram -m pip install /path/to/script/${myLibrary}.whl --target /path/to/script/myLibrary/

"""

# NumPy is pre-installed in PyRAM, but type: ignore its neccessary to avoid vs code issues.

import numpy as np # type: ignore

# Using matplotlib normally because I'm copying the code to the same folder as the matplotlib itself.

from matplotlib import pyplot as plt # type: ignore


def test_DataGenerator_sine_wave():
    """
    Tests the DataGenerator's sine_wave method for correct output length, amplitude, and frequency.

    This test creates a DataGenerator instance with 50 points, generates a sine wave with a frequency of 3 and amplitude of 2,
    and asserts that the generated x and y arrays have the correct length. It also checks that the maximum amplitude of the
    generated sine wave is approximately 2.
    """
    gen = DataGenerator(n_points=50)
    x, y = gen.sine_wave(freq=3, amp=2)

    assert len(x) == 50
    assert len(y) == 50
    # Check amplitude and frequency
    assert abs(max(y)) - 2 < 1e-6


def test_DataGenerator_cosine_wave():
    """
    Test the cosine_wave method of the DataGenerator class.
    This test verifies that the cosine_wave method generates the correct number of points,
    and that the amplitude of the generated wave matches the expected value.
    Assertions:
        - The length of the generated x and y arrays is equal to n_points (30).
        - The maximum absolute value of the y array is approximately equal to the specified amplitude (0.5).
    Raises:
        AssertionError: If any of the assertions fail.
    """


    gen = DataGenerator(n_points=30)
    x, y = gen.cosine_wave(freq=1.5, amp=0.5)
    assert len(x) == 30
    assert len(y) == 30
    assert abs(max(y)) - 0.5 < 1e-6


def test_DataGenerator_random_data():
    """
    Test the DataGenerator's random_data method.
    This test verifies that:
    - The random_data method returns two arrays, x and y, each with the specified number of points (10).
    - The y values are within the range [0, 1].
    """


    gen = DataGenerator(n_points=10)
    x, y = gen.random_data()
    assert len(x) == 10
    assert len(y) == 10
    # y should be between 0 and 1
    assert (y >= 0).all() and (y <= 1).all()


def test_Plotter_methods(monkeypatch):
    """
    Test the methods of the Plotter class to ensure that plot, scatter, legend, and show are called as expected.
    This test uses monkeypatching to replace the actual plotting methods with lambdas that record their invocation.
    It verifies that:
        - plot() is called when plotter.plot() is used,
        - scatter() is called when plotter.scatter() is used,
        - legend() is called (presumably as part of plot or scatter),
        - matplotlib.pyplot.show() is called when plotter.show() is used.
    Args:
        monkeypatch: pytest fixture for safely patching and restoring objects during the test.
    """


    plotter = Plotter(title="Test")
    called = {}

    monkeypatch.setattr(plotter.ax, "plot", lambda *a, **k: called.setdefault("plot", True))
    monkeypatch.setattr(plotter.ax, "scatter", lambda *a, **k: called.setdefault("scatter", True))
    monkeypatch.setattr(plotter.ax, "legend", lambda *a, **k: called.setdefault("legend", True))
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: called.setdefault("show", True))
    x, y = [0, 1], [1, 2]

    plotter.plot(x, y, label="lbl", style='-')
    plotter.scatter(x, y, label="lbl", color='r')
    plotter.show()

    assert called["plot"]
    assert called["scatter"]
    assert called["legend"]
    assert called["show"]


def test_MultiPlotter_methods(monkeypatch):
    """
    Test the main methods of the MultiPlotter class to ensure they call the appropriate matplotlib functions.
    This test uses monkeypatching to replace the plotting, legend, title, layout, and show methods with mocks
    that record their invocation. It verifies that:
    - The `plot` method is called when plotting on an axis.
    - The `legend` method is called after plotting.
    - The `set_title` method is called with the correct title.
    - The `tight_layout` and `show` functions from matplotlib.pyplot are called when displaying the plot.
    Args:
        monkeypatch: pytest fixture for dynamically patching objects and functions during the test.
    """


    multi = MultiPlotter(nrows=1, ncols=2)
    called = {}

    for ax in multi.axes:

        monkeypatch.setattr(ax, "plot", lambda *a, **k: called.setdefault("plot", True))
        monkeypatch.setattr(ax, "legend", lambda *a, **k: called.setdefault("legend", True))
        monkeypatch.setattr(ax, "set_title", lambda t: called.setdefault("set_title", t))

    monkeypatch.setattr("matplotlib.pyplot.tight_layout", lambda: called.setdefault("tight_layout", True))
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: called.setdefault("show", True))

    x, y = [0, 1], [1, 2]
    multi.plot_on(0, x, y, label="lbl", style='-')
    multi.set_title(0, "Title")
    multi.show()

    assert called["plot"]
    assert called["legend"]
    assert called["set_title"] == "Title"
    assert called["tight_layout"]
    assert called["show"]


def test_main_runs(monkeypatch):
    # Patch plt.show to avoid opening windows

    monkeypatch.setattr(plt, "show", lambda: None)
    main()

class DataGenerator:

    def __init__(self, n_points=100):
        """
        Initializes the object with a specified number of points.
        Parameters
        ----------
        n_points : int, optional
            The number of points to initialize with. Default is 100.
        """

        self.n_points = n_points

    def sine_wave(self, freq=1.0, amp=1.0):
        """
        Generates a sine wave based on the specified frequency and amplitude.
        Parameters:
            freq (float, optional): Frequency of the sine wave. Defaults to 1.0.
            amp (float, optional): Amplitude of the sine wave. Defaults to 1.0.
        Returns:
            tuple: A tuple (x, y) where:
                - x (numpy.ndarray): Array of points along the x-axis, ranging from 0 to 2π.
                - y (numpy.ndarray): Array of sine values corresponding to x, scaled by amplitude and frequency.
        """

        x = np.linspace(0, 2 * np.pi, self.n_points)
        y = amp * np.sin(freq * x)

        return x, y

    def cosine_wave(self, freq=1.0, amp=1.0):
        """
        Generate a cosine wave.
        Parameters:
            freq (float, optional): Frequency of the cosine wave. Default is 1.0.
            amp (float, optional): Amplitude of the cosine wave. Default is 1.0.
        Returns:
            tuple: A tuple (x, y) where:
                - x (ndarray): Array of points along the x-axis.
                - y (ndarray): Array of cosine values corresponding to x.
        """

        x = np.linspace(0, 2 * np.pi, self.n_points)
        y = amp * np.cos(freq * x)

        return x, y

    def random_data(self):
        """
        Generates random y-data and corresponding x-data for plotting or analysis.
        Returns:
            tuple: A tuple containing:
                - x (numpy.ndarray): Evenly spaced values between 0 and 10 with length `self.n_points`.
                - y (numpy.ndarray): Random values between 0 and 1 with length `self.n_points`.
        """

        x = np.linspace(0, 10, self.n_points)
        y = np.random.rand(self.n_points)

        return x, y

class Plotter:

    def __init__(self, title="Plot"):
        """
        Initializes the plot with a figure and axes, and sets the title.
        Parameters:
            title (str): The title of the plot. Defaults to "Plot".
        """

        self.fig, self.ax = plt.subplots()
        self.ax.set_title(title)

    def plot(self, x, y, label=None, style='-'):
        """
        Plots the given x and y data on the current axes.
        Parameters:
            x (array-like): The x-coordinates of the data points.
            y (array-like): The y-coordinates of the data points.
            label (str, optional): The label for the plot legend. Defaults to None.
            style (str, optional): The line style for the plot (e.g., '-', '--', 'o'). Defaults to '-'.
        Returns:
            None
        """

        self.ax.plot(x, y, style, label=label)

    def scatter(self, x, y, label=None, color='r'):
        """
        Plots a scatter plot on the current axes.
        Parameters:
            x (array-like): The x-coordinates of the points.
            y (array-like): The y-coordinates of the points.
            label (str, optional): The label for the data series. Defaults to None.
            color (str or array-like, optional): The color of the points. Defaults to 'r'.
        Returns:
            None
        """

        self.ax.scatter(x, y, label=label, color=color)

    def show(self):
        """
        Displays the plot with a legend.
        This method adds a legend to the current axes and then shows the plot window.
        """

        self.ax.legend()
        plt.show()

class MultiPlotter:

    def __init__(self, nrows=1, ncols=2, figsize=(10, 4)):
        """
        Initializes the object by creating a matplotlib figure and axes.
        Parameters:
            nrows (int, optional): Number of rows of subplots. Defaults to 1.
            ncols (int, optional): Number of columns of subplots. Defaults to 2.
            figsize (tuple, optional): Size of the figure in inches (width, height). Defaults to (10, 4).
        Attributes:
            fig (matplotlib.figure.Figure): The created matplotlib figure.
            axes (numpy.ndarray or matplotlib.axes.Axes): The created axes or array of axes.
        """

        self.fig, self.axes = plt.subplots(nrows, ncols, figsize=figsize)

    def plot_on(self, idx, x, y, label=None, style='-'):
        """
        Plots data on the specified axes.
        Parameters:
            idx (int): Index of the axes in self.axes to plot on.
            x (array-like): X-axis data.
            y (array-like): Y-axis data.
            label (str, optional): Label for the plot legend. Defaults to None.
            style (str, optional): Line style for the plot (e.g., '-', '--', 'o'). Defaults to '-'.
        Returns:
            None
        """

        ax = self.axes[idx]
        ax.plot(x, y, style, label=label)
        ax.legend()

    def set_title(self, idx, title):
        """
        Set the title of the subplot at the specified index.
        Parameters:
            idx (int): Index of the subplot whose title is to be set.
            title (str): The title to set for the specified subplot.
        """

        self.axes[idx].set_title(title)

    def show(self):
        """
        Displays the current matplotlib figure with a tight layout applied.
        This method adjusts subplot parameters to give specified padding and then renders the figure window.
        """

        plt.tight_layout()
        plt.show()

def main():
    """
    Main function to generate and plot example data using custom plotting utilities.
    This function performs the following steps:
    1. Instantiates a DataGenerator to create sample data:
        - Generates a sine wave with frequency 2 Hz and amplitude 1.
        - Generates a cosine wave with frequency 2 Hz and amplitude 0.5.
        - Generates random data points.
    2. Creates a single plot using Plotter:
        - Plots the sine wave with a blue solid line.
        - Plots the cosine wave with a green dashed line.
        - Plots the random data as red scatter points.
        - Displays the plot with the title "Sine and Cosine Waves".
    3. Creates multiple subplots using MultiPlotter:
        - Plots the sine wave in the first subplot with the title "Sine Wave".
        - Plots the cosine wave in the second subplot with the title "Cosine Wave".
        - Displays the subplots.
    """

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