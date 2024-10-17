from gs_process.utils.common import *
import open3d as o3d
import os
import yaml


class Dataloader:
    def __init__(self, config=config, params=params, ransac=False, dbscan=False):
        """
                Initialize the Dataloader class.
        .
        """

        self.normalize = config["process"]["normalize"]  # Whether to normalize
        self.save_norm = config["process"][
            "save_norm"
        ]  # Whether to save the normalized point cloud
        self.params = params  # Store the parameters

        if ransac and self.save_norm:
            self.pcl_path = config[
                "norm_pcl_path"
            ]  # Path to the normalized point cloud file
        elif dbscan:
            self.pcl_path = config[
                "ransac_pcl_path"
            ]  # Path to the normalized ransac point cloud file
        else:
            self.pcl_path = config["pcl_path"]  # raw pcl

    def load_point_cloud(self):
        """
        Load the point cloud from the specified file path.

        Returns:
            pcl (open3d.geometry.PointCloud): The loaded point cloud object.
        """
        # Load the point cloud from the specified file path
        pcl = o3d.io.read_point_cloud(self.pcl_path)
        print(f"Loaded point cloud type: {type(pcl)}")
        return pcl

    def normalize_and_save(self, pcl):
        """
        Normalize the point cloud and save it to a file if specified.

        Args:
            pcl (open3d.geometry.PointCloud): The point cloud object to be normalized.
        """
        if self.normalize:
            # Set up parameters for estimate_normals from params.yaml
            search_param = self.params["estimate_normals"]["search_param"]
            radius = search_param["radius"]
            max_nn = search_param["max_nn"]
            fast_normal_computation = self.params["estimate_normals"][
                "fast_normal_computation"
            ]

            # Estimate normals for the point cloud
            print("Estimating normals...")
            pcl.estimate_normals(
                search_param=o3d.geometry.KDTreeSearchParamHybrid(
                    radius=radius, max_nn=max_nn
                ),
                fast_normal_computation=fast_normal_computation,
            )

            # Apply a uniform color to the point cloud from params.yaml
            color = self.params["estimate_normals"]["paint_uniform_color"]["color"]
            print(f"Applying uniform color: {color}")
            pcl.paint_uniform_color(color)

            # Save the normalized point cloud if save_norm is True
            if self.save_norm:
                # Get the base name of the input file (without extension)
                input_filename = os.path.basename(self.pcl_path)
                input_name, input_ext = os.path.splitext(input_filename)

                # Create the output folder if it doesn't exist
                output_dir = "output"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Save the normalized point cloud with "_normalized" added to the filename
                output_file = os.path.join(output_dir, f"{input_name}_normalized.ply")
                success = o3d.io.write_point_cloud(output_file, pcl)

                if success:
                    print(f"Normalized point cloud saved to {output_file}")
                else:
                    print(f"Failed to save the normalized point cloud to {output_file}")


if __name__ == "__main__":
    """
    Main execution function that initializes the Dataloader class,
    loads the point cloud, normalizes it, and saves it if required.
    """
    dl = (
        Dataloader()
    )  # Initialize the Dataloader class with default config and params file paths
    pcl = dl.load_point_cloud()  # Load the point cloud
    dl.normalize_and_save(pcl)  # Normalize and save the point cloud
