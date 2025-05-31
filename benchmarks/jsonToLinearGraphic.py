import json
"""
jsonToLinearGraphic.py
This module provides the JsonToLinearGraphic class, which reads benchmark data from a JSON file and generates linear (line) plots for each test case found in the data. The resulting plots are saved as PNG images in a structured output directory.
Classes:
    JsonToLinearGraphic: Handles loading JSON data, validating its structure, plotting the data using matplotlib, and saving the resulting images.
Usage:
    Run this script from the command line with the following arguments:
        python jsonToLinearGraphic.py <input_json_file> <output_image_name>
Arguments:
    <input_json_file>: Path to the input JSON file containing benchmark data.
    <output_image_name>: Base name for the output image files.
    FileNotFoundError: If the specified JSON file does not exist.
    ValueError: If the input file is not a JSON file, is not a file, or if the data format is invalid.
Example JSON input format:
{
    "test1": [
        {"input": 100, "time": 0.01},
        {"input": 200, "time": 0.02}
    ],
    "test2": [
        {"input": 100, "time": 0.015},
        {"input": 200, "time": 0.025}
    ]
}
"""
import os
import sys

from typing import List, Dict

from pathlib import Path

from os import makedirs

# The import is explained in the externWHLs test 
from matplotlib import pyplot as plt # type: ignore

class JsonToLinearGraphic:
    """
    Class to convert JSON data to a linear graphic.
    """

    def __init__(self, json_path: Path, output_path: Path):
        """
        Initialize the JsonToLinearGraphic class.
        :param json_path: Path to the JSON file.
        :param output_path: Path to save the output image.
        """

        self.json_path = json_path
        self.data: Dict[str, List[Dict[str, float|int]]] = self.load_data()
        self.output_image = output_path


        for test_name in self.data.keys():

            if not isinstance(self.data[test_name], list):

                raise ValueError(f"Invalid data format for test '{test_name}'. Expected a list.")
            
            if len(self.data[test_name]) == 0:

                raise ValueError(f"No data found for test '{test_name}'.")

            labels: List[str] = [str(item['input']) for item in self.data[test_name]]
            values: List[str] = [str(item['time']) for item in self.data[test_name]]

            self.plot(labels, values, test_name)



    def load_data(self):
        """
        Load data from the JSON file.
        :return: Parsed JSON data.
        """

        if not os.path.exists(self.json_path):

            raise FileNotFoundError(f"JSON file not found: {self.json_path}")
        
        if not str(self.json_path).endswith('.json'):

            raise ValueError(f"Invalid file format: {self.json_path}. Expected a .json file.")
        
        if not os.path.isfile(self.json_path):

            raise ValueError(f"Invalid file path: {self.json_path}. Expected a file.")
        


        with open(self.json_path, 'r') as f:

            return json.load(f)
        

    def plot(self, labels: List[str], values: List[str], test: str):
        """
        Plot the data as a linear graphic.
        :param labels: Labels for the x-axis.
        :param values: Values for the y-axis.
        """

        plt.figure(figsize=(10, 6))
        plt.plot(labels, values, marker='o', linestyle='-', color='b')

        self._set_plot_labels(test)
        self._save_plot(test)

        plt.close()

    def _set_plot_labels(self, test_name: str):
        """
        Sets the labels and title for the plot using matplotlib.
        Parameters:
            test_name (str): The title to be displayed on the plot.
        This method sets the x-axis label to 'Input Size', the y-axis label to 'Time (seconds)',
        applies the provided test name as the plot title, enables the grid, and adjusts the layout
        for better appearance.
        """

        plt.xlabel('Input Size')
        plt.ylabel('Time (seconds)')
        plt.title(test_name)

        plt.grid(True)

        plt.tight_layout()

    def _save_plot(self, test_name: str):
        """
        Saves the current matplotlib plot to a PNG file in the appropriate output directory.
        Args:
            test_name (str): The name of the test, used to construct the output file path.
        Side Effects:
            - Creates the output directory if it does not exist.
            - Saves the current matplotlib figure as a PNG image file with a name based on `self.output_image` and `test_name`.
        Raises:
            OSError: If the output directory cannot be created or the image cannot be saved.
        """

        out_path: Path = (Path(__file__).parent.parent / 'data' / f'{test_name}').resolve()
        output_image = out_path / f'{self.output_image}_{test_name}.png'
        makedirs(str(output_image.parent), exist_ok=True)

        plt.savefig(output_image)

if __name__ == "__main__":


    try:
        if len(sys.argv) != 3:
            raise ValueError("Usage: python jsonToLinearGraphic.py <input_json_file> <output_image_name>")
        
        graphic = JsonToLinearGraphic(Path(sys.argv[1]), Path(sys.argv[2]))

    except Exception as e:
        
        print(f"Error: {e}")
        sys.exit(1)
