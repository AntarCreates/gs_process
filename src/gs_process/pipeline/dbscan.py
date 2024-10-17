import os
from gs_process.utils.common import*
from gs_process.pipeline.dataloader import Dataloader

class DBSCANProcessor:
    def __init__(self, config=config, params=params):
        self.config = config
        self.params = params
        self.save_dbscan = config['process']['save_dbscan']

    def process_dbscan(self, object_cloud):
        # Set up parameters for DBSCAN from params.yaml
        eps = self.params['cluster_dbscan']['eps']
        min_points = self.params['cluster_dbscan']['min_points']

        print(f"Performing DBSCAN with eps={eps} and min_points={min_points}...")
        
        # Perform DBSCAN clustering
        labels = np.array(object_cloud.cluster_dbscan(eps=eps, min_points=min_points))
        
        # Number of clusters
        max_label = labels.max()
        print(f"Point cloud has {max_label + 1} clusters")
        
        # Color each cluster using a colormap
        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        
        # Noise clusters (label -1) are colored white
        colors[labels < 0] = 1
        
        # Apply the colors to the point cloud
        object_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])

        if self.save_dbscan:
            # Get the base name of the input file (without extension)
            input_filename = os.path.basename(self.config['pcl_path'])
            input_name, input_ext = os.path.splitext(input_filename)

            # Create the output folder if it doesn't exist
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the clustered point cloud with "_dbscan" added to the filename
            output_file = os.path.join(output_dir, f"{input_name}_dbscan.ply")
            success = o3d.io.write_point_cloud(output_file, object_cloud)

            if success:
                print(f"DBSCAN processed point cloud saved to {output_file}")
            else:
                print(f"Failed to save the DBSCAN processed point cloud to {output_file}")

if __name__ == "__main__":
    # Load the point cloud using the Dataloader
    dl = Dataloader(dbscan=True)
    pcl_ransac = dl.load_point_cloud()
    
    # Assume the point cloud has already been segmented by RANSAC
    # Object cloud is passed to DBSCAN
    dbscan_processor = DBSCANProcessor(config, params)
    dbscan_processor.process_dbscan(pcl_ransac)
