from gs_process.pipeline.dataloader import Dataloader
from gs_process.utils.common import*


class RANSACProcessor:
    def __init__(self, dataloader, config=config, params=params):
        """
        Initialize the RANSAC processor with the given Dataloader, config, and params.
        Args:
            dataloader (Dataloader): Instance of the Dataloader class for loading the point cloud.
            config (dict): Dictionary with configuration settings.
            params (dict): Dictionary with parameters for RANSAC.
        """
        self.dataloader = dataloader
        self.pcl_path = dataloader.pcl_path
        self.save_ransac = config["process"]["save_ransac"]
        self.params = params

    def apply_ransac(self, pcl):
        """
        Apply RANSAC segmentation to the point cloud.
        Args:
            pcl (open3d.geometry.PointCloud): Input point cloud to process.
        """
        # Set up parameters for RANSAC from params.yaml
        distance_threshold = self.params['segment_plane']['distance_threshold']
        ransac_n = self.params['segment_plane']['ransac_n']
        num_iterations = self.params['segment_plane']['num_iterations']

        # Detect planes and shapes using RANSAC
        print("Applying RANSAC...")
        plane, object_indices = pcl.segment_plane(
            distance_threshold=distance_threshold, 
            ransac_n=ransac_n, 
            num_iterations=num_iterations
        )

        # Extract object and noise clouds
        object_cloud = pcl.select_by_index(object_indices)
        noise_cloud = pcl.select_by_index(object_indices, invert=True)

        # Paint the detected shapes and noise cloud with colors from params.yaml
        object_color = self.params["segment_plane"]['colors']['object_cloud']
        noise_color = self.params["segment_plane"]['colors']['noise_cloud']
        
        object_cloud.paint_uniform_color(object_color)
        noise_cloud.paint_uniform_color(noise_color)

        if self.save_ransac:
            # Save the RANSAC-processed point clouds
            input_filename = os.path.basename(self.pcl_path)
            input_name, input_ext = os.path.splitext(input_filename)

            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save object cloud and noise cloud
            object_output_file = os.path.join(output_dir, f"{input_name}_ransac_object.ply")
            noise_output_file = os.path.join(output_dir, f"{input_name}_ransac_noise.ply")
            
            o3d.io.write_point_cloud(object_output_file, object_cloud)
            o3d.io.write_point_cloud(noise_output_file, noise_cloud)

            print(f"RANSAC object cloud saved to {object_output_file}")
            print(f"RANSAC noise cloud saved to {noise_output_file}")

        # Visualize the object and noise clouds (optional)
        # o3d.visualization.draw_geometries([object_cloud, noise_cloud])

if __name__ == "__main__":
    # Initialize Dataloader and RANSACProcessor
    dl = Dataloader(ransac=True)
    pcl_norm = dl.load_point_cloud()
    # Apply RANSAC processing
    ransac_processor = RANSACProcessor(dl)
    ransac_processor.apply_ransac(pcl_norm)
