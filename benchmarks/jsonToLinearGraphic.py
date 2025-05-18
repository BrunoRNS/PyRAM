import json
import os

import matplotlib.pyplot as plt

# Path to the JSON file created by benchmarks.py
json_path = os.path.join(os.path.dirname(__file__), 'benchmarks.json')

# Load data from JSON
with open(json_path, 'r') as f:
    data = json.load(f)


# Example: {"test1": 1.2, "test2": 2.3, ...}
labels = list(data.keys())
values = list(data.values())

# Plot linear graphic
plt.figure(figsize=(10, 6))
plt.plot(labels, values, marker='o', linestyle='-', color='b')
plt.xlabel('Benchmark')
plt.ylabel('Value')
plt.title('Benchmarks Linear Graphic')
plt.grid(True)
plt.tight_layout()

# Save the image
output_image = os.path.join(os.path.dirname(__file__), 'benchmarks_linear_graphic.png')
plt.savefig(output_image)
plt.close()