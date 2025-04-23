# Interactive plotting tool for Bicriteria Aggregation solutions
This interactive visualization tool was developed as part of our paper 'Parameterized Algorithms for Computing Pareto Sets' (link to be added). It visualizes solutions produced by the Bicriteria Aggregation algorithm.

## About
The tool provides an interactive way to explore and analyze solutions computed by the Bicriteria Aggregation algorithm. Due to GitHub's file size limitations, only the Osterloh dataset is included, as it has the smallest solutions output file.

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
- Python 3.7+ (Recommended)
The code may also run with lower versions, but this has not been tested.

- numpy
- pandas
- matplotlib
- geopandas
- shapely
- (Optional: Git LFS)

## Setup
The file osterloh/solutions_labeled_osterloh.csv is tracked using Git LFS due to its size (~400 MB).
If you clone the repository via Git (with Git LFS installed), the full file will be downloaded automatically.

However, if you download the repository as a ZIP archive, Git LFS files are not included. Instead, you will get a small placeholder .csv file.

To work around this, a compressed version of the actual CSV is provided in osterloh/solutions_labeled_osterloh.zip.
To use the tool:
1. Extract the ZIP file.
2. Replace the placeholder file osterloh/solutions_labeled_osterloh.csv with the extracted CSV.

## Running the tool
Simply execute the script using Python:

```bash
python shape-plotting.py
```

