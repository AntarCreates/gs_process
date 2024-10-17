from gs_process.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
import open3d as o3d
import numpy as np
import yaml
import os
import matplotlib.pyplot as plt


# Function to read YAML file
def read_yaml(file_path):
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            return data
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return None


# set config and params
config = read_yaml(CONFIG_FILE_PATH)
params = read_yaml(PARAMS_FILE_PATH)
