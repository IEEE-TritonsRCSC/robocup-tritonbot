import matplotlib
matplotlib.use('TKAgg') # Use X11 backend for real time data forwarding
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation
from matplotlib import style
style.use('dark_background')
import os
from random import randint


class Plotter:
    def __init__(self):
        """
        Constructor 
        
        expectedWheelVelocities1 - List of all expected wheel 1 velocities received
        actualWheelVelocities1 - List of all actual wheel 1 velocities received
        
        expectedWheelVelocities2 - List of all expected wheel 2 velocities received
        actualWheelVelocities2 - List of all actual wheel 2 velocities received
        
        expectedWheelVelocities3 - List of all expected wheel 3 velocities received
        actualWheelVelocities3 - List of all actual wheel 3 velocities received
        
        expectedWheelVelocities4 - List of all expected wheel 4 velocities received
        actualWheelVelocities4 - List of all actual wheel 4 velocities received
        
        expectedWheel1 - line plot for expected wheel 1 data
        actualWheel1 - line plot for actual wheel 1 data
        
        expectedWheel2 - line plot for expected wheel 2 data
        actualWheel2 - line plot for actual wheel 2 data
        
        expectedWheel3 - line plot for expected wheel 3 data
        actualWheel3 - line plot for actual wheel 3 data
        
        expectedWheel4 - line plot for expected wheel 4 data
        actualWheel4 - line plot for actual wheel 4 data
        
        fig - container for all 4 graphs
        axs - axis for all 4 wheels
        
        anim - graph animation 
        """
        
        # Initialize empty lines for t and all actual and expected wheel velocities
        self.t = []
        
        self.expectedWheelVelocities1 = []
        self.actualWheelVelocities1 = []
        
        self.expectedWheelVelocities2 = []
        self.actualWheelVelocities2 = []
        
        self.expectedWheelVelocities3 = []
        self.actualWheelVelocities3 = []
        
        self.expectedWheelVelocities4 = []
        self.actualWheelVelocities4 = []

        # Create a figure and axis for all 4 wheels
        self.fig, self.axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

        # Create an empty line
        #self.line_expected, = self.ax.plot([], [], label='expected wheel 1', color='green')
        #self.line_actual, = self.ax.plot([], [], label='actual wheel 1', color='red')
        
        # Plot on the first subplot (Wheel 1 top-left)
        self.expectedWheel1 = self.axs[0, 0].plot(self.t, self.expectedWheelVelocities1, label='Expected', color='green')
        self.actualWheel1 = self.axs[0, 0].plot(self.t, self.actualWheelVelocities1, label='Actual', color='red')
        self.axs[0, 0].set_title('Wheel 1 Velocities')
        self.axs[0, 0].set_xlabel('Time (s)')
        self.axs[0, 0].set_ylabel('Velocity (RPM)')
        self.axs[0, 0].legend()

        # Plot on the second subplot (Wheel 2 top-right)
        self.expectedWheel2 = self.axs[0, 1].plot(self.t, self.expectedWheelVelocities2, label='Expected', color='green')
        self.actualWheel2 = self.axs[0, 1].plot(self.t, self.actualWheelVelocities2, label='Actual', color='red')
        self.axs[0, 1].set_title('Wheel 2 Velocities')
        self.axs[0, 1].set_xlabel('Time (s)')
        self.axs[0, 1].set_ylabel('Velocity (RPM)')
        self.axs[0, 1].legend()

        # Plot on the third subplot (Wheel 3 bottom-left)
        self.expectedWheel3 = self.axs[1, 0].plot(self.t, self.expectedWheelVelocities3, label='Expected', color='green')
        self.actualWheel3 = self.axs[1, 0].plot(self.t, self.actualWheelVelocities3, label='Actual', color='red')
        self.axs[1, 0].set_title('Wheel 3 Velocities')
        self.axs[1, 0].set_xlabel('Time (s)')
        self.axs[1, 0].set_ylabel('Velocity (RPM)')
        self.axs[1, 0].legend()

        # Plot on the fourth subplot (Wheel 4 bottom-right)
        self.expectedWheel4 = self.axs[1, 1].plot(self.t, self.expectedWheelVelocities4, label='Expected', color='green')
        self.actualWheel4 = self.axs[1, 1].plot(self.t, self.actualWheelVelocities4, label='Actual', color='red')
        self.axs[1, 1].set_title('Wheel 4 Velocities')
        self.axs[1, 1].set_xlabel('Time (s)')
        self.axs[1, 1].set_ylabel('Velocity (RPM)')
        self.axs[1, 1].legend()

        plt.tight_layout()
        
        for ax in self.axs.flat:
            ax.set_xlim(0, 150)
            ax.set_ylim(2000, 12000)

        # Create the animation
        self.anim = animation(self.fig, self.update_plot, frames=100, interval=1000, repeat=False)
        
    
    def extractVelocities(self, expected, actual):
        """
        This function is designed to extract velocities from hexadecimal
        values representing expected and actual velocities.
        
        :param expected: The `expected` parameter likely
        represents the expected velocity in hexadecimal format. This parameter may
        contain the expected velocity value encoded in hexadecimal
        :param actual: The `actual` parameter likely
        represents the actual velocity in hexadecimal format. To extract the
        velocities from the hexadecimal format, you can convert the hexadecimal
        values to decimal values.
        
        TODO (Current implementation plots random values)
        """
        
        
        expectedVelocities, actualVelocities = [], []
        
        expectedVelocities.append(expected - randint(1, 20)) # random numbers for testing purposes
        actualVelocities.append(actual + randint(1, 20))

        expectedVelocities.append(expected - randint(1, 20))
        actualVelocities.append(actual + randint(1, 20))
        
        expectedVelocities.append(expected - randint(1, 20))
        actualVelocities.append(actual + randint(1, 20))
        
        expectedVelocities.append(expected - randint(1, 20))
        actualVelocities.append(actual - randint(1, 20))
        
        return expectedVelocities, actualVelocities


    def update_plot(self, frame, expectedVelocities, actualVelocities):
        """
        This function updates a plot with the given frame, expected wheel
        velocities, and actual wheel velocities.
        
        :param frame: The `frame` parameter refers to the current frame or
        time step of the plot being updated. It is used to determine at which point
        in the plot the data should be updated

        expectedWheelVelocity1 - expected wheel 1 velocities received
        actualWheelVelocity1 - actual wheel 1 velocities received
        
        expectedWheelVelocity2 - expected wheel 2 velocities received
        actualWheelVelocity2 - actual wheel 2 velocities received
        
        expectedWheelVelocity3 - expected wheel 3 velocities received
        actualWheelVelocity3 - actual wheel 3 velocities received
        
        expectedWheelVelocity4 - expected wheel 4 velocities received
        actualWheelVelocity4 - actual wheel 4 velocities received
        """
        
        t = frame
        
        #expectedVelocities, actualVelocities = self.extractVelocities(expectedWheelVelocities, actualWheelVelocities)
        
        expectedWheelVelocity1 = expectedVelocities[0]
        actualWheelVelocity1 = actualVelocities[0]

        expectedWheelVelocity2 = expectedVelocities[1]
        actualWheelVelocity2 = actualVelocities[1]
        
        expectedWheelVelocity3 = expectedVelocities[2]
        actualWheelVelocity3 = actualVelocities[2]
        
        expectedWheelVelocity4 = expectedVelocities[3]
        actualWheelVelocity4 = actualVelocities[3]

        # Append data to lists
        self.t.append(t)
        
        self.expectedWheelVelocities1.append(expectedWheelVelocity1)
        self.actualWheelVelocities1.append(actualWheelVelocity1)
        
        self.expectedWheelVelocities2.append(expectedWheelVelocity2)
        self.actualWheelVelocities2.append(actualWheelVelocity2)
        
        self.expectedWheelVelocities3.append(expectedWheelVelocity3)
        self.actualWheelVelocities3.append(actualWheelVelocity3)
        
        self.expectedWheelVelocities4.append(expectedWheelVelocity4)
        self.actualWheelVelocities4.append(actualWheelVelocity4)

    
        # Update line data
        self.expectedWheel1[0].set_data(self.t, self.expectedWheelVelocities1)
        self.actualWheel1[0].set_data(self.t, self.actualWheelVelocities1)
        
        self.expectedWheel2[0].set_data(self.t, self.expectedWheelVelocities2)
        self.actualWheel2[0].set_data(self.t, self.actualWheelVelocities2)
        
        self.expectedWheel3[0].set_data(self.t, self.expectedWheelVelocities3)
        self.actualWheel3[0].set_data(self.t, self.actualWheelVelocities3)
        
        self.expectedWheel4[0].set_data(self.t, self.expectedWheelVelocities4)
        self.actualWheel4[0].set_data(self.t, self.actualWheelVelocities4)
    

        # Adjust view limits if needed (TODO)
        for ax in self.axs.flat:
            ax.relim()
            ax.autoscale_view()

        plt.pause(0.0001)

    def save(self, filename='output.png'):
        """
        This function saves an image to a specified filename, with a default
        filename of 'output.png'.
        
        :param filename: The `save` method is used to save an image to a file. The
        `filename` parameter specifies the name of the file where the image will be
        saved. By default, the image will be saved as 'output.png' if no filename is
        provided when calling the method, defaults to output.png (optional)
        """
        save_dir = "saved_graphs"
        os.makedirs(save_dir, exist_ok=True)
        # Save the figure to a PNG file
        filename = filename if filename else "output.png"
        save_path = os.path.abspath(os.path.join(save_dir, filename))
        self.fig.savefig(save_path)
        # self.fig.savefig(os.path.join("saved_graphs", filename))
