#!/usr/bin/python3
import pigpio
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

# GPIO pin numbers for the stepper motor connections
in1 = 26
in2 = 16
in3 = 6
in4 = 5
in5 = 23
in6 = 22
in7 = 27
in8 = 17

# Delay between steps for different speeds
step_sleep = 0.002
step_sleep1 = 0.001

# Number of steps for different sequences
step_count = 4096
step_count1 = 4710

# Direction variables
direction1 = True
direction2 = True

motor_step_counter = 0

# Define the step sequence for the stepper motor
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# Initialize pigpio
pi = pigpio.pi()

# Function to clean up GPIO pins
def cleanup():
    for pin in [in1, in2, in3, in4, in5, in6, in7, in8]:
        pi.write(pin, 0)
    pi.stop()

def stepper():
    try:
        # Rotate the stepper motor in one direction
        direction2 = True
        for _ in range(step_count1):
            for pin, value in zip([in5, in6, in7, in8], step_sequence[motor_step_counter]):
                pi.write(pin, value)
            if direction2:
                motor_step_counter = (motor_step_counter - 1) % 8
                #step_sequence = step_sequence[-1:] + step_sequence[:-1]
            else:
                motor_step_counter = (motor_step_counter + 1) % 8
                #step_sequence = step_sequence[1:] + step_sequence[:1]
            time.sleep(step_sleep1)

        # Rotate the stepper motor in the other direction
        direction1 = True
        for _ in range(step_count):
            for pin, value in zip([in1, in2, in3, in4], step_sequence[motor_step_counter]):
                pi.write(pin, value)
            if direction1:
                #step_sequence = step_sequence[-1:] + step_sequence[:-1]
                motor_step_counter = (motor_step_counter - 1) % 8
            else:
                #step_sequence = step_sequence[1:] + step_sequence[:1]
                motor_step_counter = (motor_step_counter + 1) % 8
            time.sleep(step_sleep)

        # Rotate back in the first direction
        direction2 = False
        for _ in range(step_count1):
            for pin, value in zip([in5, in6, in7, in8], step_sequence[motor_step_counter]):
                pi.write(pin, value)
            if direction2:
                #step_sequence = step_sequence[-1:] + step_sequence[:-1]
                motor_step_counter = (motor_step_counter - 1) % 8
            else:
                motor_step_counter = (motor_step_counter + 1) % 8
                #step_sequence = step_sequence[1:] + step_sequence[:1]
            time.sleep(step_sleep1)

        # Print finish message
        print('Finish')

    except KeyboardInterrupt:
        # Cleanup GPIO pins if keyboard interrupt occurs
        cleanup()
        exit(1)

    # Cleanup GPIO pins and exit
    cleanup()

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        stepper()


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()