import json
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

        test_name: str = test

        plt.figure(figsize=(10, 6))
        plt.plot(labels, values, marker='o', linestyle='-', color='b')

        plt.xlabel('Input Size')
        plt.ylabel('Time (seconds)')

        plt.title(test_name)

        plt.grid(True)
        plt.tight_layout()

        # because the script will be copied to the matplotlib folder
        out_path: Path = (Path(__file__).parent.parent / 'data' / f'{test_name}').resolve() 

        output_image = out_path / f'{self.output_image}_{test_name}.png'

        makedirs(str(output_image.parent), exist_ok=True)

        plt.savefig(output_image)
        plt.close()

if __name__ == "__main__":

    try:
        if len(sys.argv) != 3:
            raise ValueError("Usage: python jsonToLinearGraphic.py <input_json_file> <output_image_name>")
        
        graphic = JsonToLinearGraphic(Path(sys.argv[1]), Path(sys.argv[2]))

    except Exception as e:
        
        print(f"Error: {e}")
        sys.exit(1)
