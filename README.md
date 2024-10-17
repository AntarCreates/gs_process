# gs_processing


This project implements a simple pipeline for point cloud processing using **Open3D** and **DVC** for reproducibility. The pipeline has three key stages: dataloader, plane segmentation using RANSAC, and clustering using DBSCAN. All configurations are managed via the `params.yaml` file.

## Project Structure
├── src │ ├── gs_processing │ │ ├── pipeline │ │ │ ├── dataloader.py # Loads point clouds │ │ │ ├── ransac.py # Applies RANSAC for plane segmentation │ │ │ ├── dbscan.py # DBSCAN clustering ├── output # Stores processed output files ├── params.yaml # Configures hyperparameters ├── dvc.yaml # DVC pipeline configuration ├── README.md # Project documentation


## Requirements

- **Python 3.8+**
- **Open3D**
- **DVC**
- **NumPy**
- **Matplotlib**

You can install the required libraries using the following command:

```bash
pip install -r requirements.txt

## Running the Pipeline

To run the pipeline, follow these steps:

### 1. Initialize DVC

First, initialize DVC in your project directory:

```bash
dvc init

### 2. Run the Pipeline
To execute the full point cloud processing pipeline, use:

```bash
dvc repro