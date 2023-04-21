import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
import numpy as np

class MapNode(Node):
    def __init__(self):
        super().__init__('MapNode')

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.publisher = self.create_publisher(OccupancyGrid, '/map', 10)

        # Initialize the occupancy grid
        self.occupancy_grid = OccupancyGrid()
        self.occupancy_grid.header.frame_id = 'map'
        self.occupancy_grid.info.resolution = 0.05
        self.occupancy_grid.info.width = 100
        self.occupancy_grid.info.height = 100
        self.occupancy_grid.info.origin.position.x = -2.5
        self.occupancy_grid.info.origin.position.y = -2.5
        self.occupancy_grid.data = [-1] * (self.occupancy_grid.info.width * self.occupancy_grid.info.height)

    def scan_callback(self, msg):
        # Convert the laser scan to occupancy grid cells
        ranges = np.array(msg.ranges)
        angles = np.linspace(msg.angle_min, msg.angle_max, len(ranges))
        x = ranges * np.cos(angles) / self.occupancy_grid.info.resolution + self.occupancy_grid.info.width / 2.0
        y = ranges * np.sin(angles) / self.occupancy_grid.info.resolution + self.occupancy_grid.info.height / 2.0
        x = np.round(x).astype(np.int)
        y = np.round(y).astype(np.int)

        # Update the occupancy grid
        for i in range(len(x)):
            if x[i] >= 0 and x[i] < self.occupancy_grid.info.width and y[i] >= 0 and y[i] < self.occupancy_grid.info.height:
                index = x[i] + y[i] * self.occupancy_grid.info.width
                self.occupancy_grid.data[index] = 100

        # Publish the occupancy grid
        self.publisher.publish(self.occupancy_grid)

def main(args=None):
    rclpy.init(args=args)
    node = MapNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
