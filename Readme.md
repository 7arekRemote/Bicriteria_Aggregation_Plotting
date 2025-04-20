# Interactive plotting tool for Bicriteria Aggregation solutions
This interactive visualization tool was developed as part of our paper 'Parameterized Algorithms for Computing Pareto Sets' (link to be added). It visualizes solutions produced by the Bicriteria Aggregation algorithm.

## About
The tool provides an intuitive way to explore and analyze solutions computed by the Bicriteria Aggregation algorithm. Due to GitHub's file size limitations, only the Osterloh dataset is included, as it has the smallest solutions output file.

## Features
- Left view: Geometric visualization of a selected solution:

    - Dark gray polygons with black borders represent buildings.

    - Light gray triangles with red borders represent the triangles used in the current solution.

- Right view: A scatter plot of all computed Pareto-optimal solutions, distinguishing between extreme and non-extreme ones.

- Mouse interactions (on the right plot):

    - Scroll wheel: Zoom in/out.

    - Left click: Select the closest non-extreme solution to the cursor. The selected solution is displayed on the left.

    - Right click: Select the closest extreme solution to the cursor. The selected solution is displayed on the left.

## Requirements
- Python 3.x
- Git LFS

- numpy
- pandas
- matplotlib
- geopandas
- shapely

## Running the tool
Simply execute the script using Python:

```bash
python shape-plotting.py
```

