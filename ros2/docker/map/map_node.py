import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
import numpy as np

class MapNode(Node):

    def __init__(self):
        super().__init__('map_node')
        self.subscription = self.create_subscription(
            LaserScan,
            '/laserscan',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(OccupancyGrid, '/map', 10)
        self.occupancy_grid_ = None

    def listener_callback(self, msg):
        # Konvertiere die LaserScan-Daten in eine 2D-Map
        map_resolution = 0.05 # 5 cm pro Zelle
        map_size = 100 # 5 m x 5 m Karte
        map_origin = [map_size / 2.0, map_size / 2.0, 0.0]
        map_data = np.zeros((map_size, map_size), dtype=np.int8)
        max_range = msg.range_max
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
        ranges = msg.ranges
        for i, range_value in enumerate(ranges):
            if range_value < max_range:
                angle = angle_min + i * angle_increment
                x = range_value * np.cos(angle) + map_size / 2.0
                y = range_value * np.sin(angle) + map_size / 2.0
                map_data[int(x / map_resolution), int(y / map_resolution)] = 100

        # Erstelle die OccupancyGrid-Nachricht
        if self.occupancy_grid_ is None:
            self.occupancy_grid_ = OccupancyGrid()
            self.occupancy_grid_.header.frame_id = 'map'
            self.occupancy_grid_.info.resolution = map_resolution
            self.occupancy_grid_.info.width = map_size
            self.occupancy_grid_.info.height = map_size
            self.occupancy_grid_.info.origin.position.x = -map_origin[0] * map_resolution
            self.occupancy_grid_.info.origin.position.y = -map_origin[1] * map_resolution
            self.occupancy_grid_.info.origin.position.z = 0.0
            self.occupancy_grid_.info.origin.orientation.x = 0.0
            self.occupancy_grid_.info.origin.orientation.y = 0.0
            self.occupancy_grid_.info.origin.orientation.z = 0.0
            self.occupancy_grid_.info.origin.orientation.w = 1.0
        self.occupancy_grid_.data = list(map_data.ravel())

        # Veröffentliche die Karte
        self.publisher_.publish(self.occupancy_grid_)

def main(args=None):
    rclpy.init(args=args)
    node = MapNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
