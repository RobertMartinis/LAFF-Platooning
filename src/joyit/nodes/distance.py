#!/usr/bin/env python3
import rospy

from sensor_msgs.msg import Range

from joyit.ultrasonic_driver import UltrasonicDriver

class DistanceController:
    def __init__(self):
        self.driver = UltrasonicDriver(
            rospy.get_param("GPIO5"),
            rospy.get_param("GPIO6"))

        self.distance_publisher = rospy.Publisher(
            "vehicle/distance",
            Range,
            queue_size=rospy.get_param("MESSAGE_QUEUE_SIZE"))
        self.relative_velocity_publisher = rospy.Publisher(
            "vehicle/relative_velocity",
            Range,
            queue_size=rospy.get_param("MESSAGE_QUEUE_SIZE"))

        rospy.Timer(rospy.Duration(rospy.get_param("DISTANCE_PUBLISH_PERIOD")), self.publish_current_distance)
        rospy.Timer(rospy.Duration(
                            rospy.get_param("RELATIVE_VELOCITY_PUBLISH_PERIOD")),
                            self.publish_current_velocity)

    def publish_current_distance(self, event):
        """
        Publishes the current distance to the vehicle/distance topic.
        """
        distance = self.driver.get_distance()

        rospy.loginfo(f"Distance: {distance} cm")

        r = Range()
        r.header.stamp = rospy.Time.now()
        r.header.frame_id = "/base_link"
        r.radiation_type = Range.ULTRASOUND
        r.field_of_view = self.driver.fov
        r.min_range = self.driver.min_range
        r.max_range = self.driver.max_range
        r.range = distance

        self.distance_publisher.publish(r)

    def publish_current_velocity(self, event):
        """
        Publishes the current relative velocity to the vehicle/relative_velocity topic.
        """
        relative_velocity = self.driver.get_speed()

        rospy.loginfo(f"Speed: {relative_velocity} m/s")

        r = Range()
        r.header.stamp = rospy.Time.now()
        r.header.frame_id = "/base_link"
        r.radiation_type = Range.ULTRASOUND
        r.field_of_view = self.driver.fov
        r.min_range = self.driver.min_range
        r.max_range = self.driver.max_range
        r.range = relative_velocity

        self.relative_velocity_publisher.publish(r)

    def stop(self):
        """
        Stops the distance node.
        """
        self.distance_publisher.unregister()
        self.relative_velocity_publisher.unregister()
        self.driver.cleanup()


if __name__ == "__main__":
    rospy.init_node("distance_node")
    controller = DistanceController()
    rospy.on_shutdown(controller.stop)

    rospy.loginfo("Distance node started.")
    rospy.spin()
