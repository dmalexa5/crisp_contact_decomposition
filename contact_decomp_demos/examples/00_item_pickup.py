# %%
import time
import os
import numpy as np

from crisp_py.robot import make_robot

robot = make_robot("fr3")
robot.wait_until_ready()

# %%
input("Press Enter to go to home position... ")
robot.home()
homing_pose = robot.end_effector_pose.copy()

# %%
print(robot.end_effector_pose)
print(robot.joint_values)

# %%
# Parameters for pickup location
pickup_point = np.array([0.45, 0.0, 0.17])
ctrl_freq = 50.0

# %%
robot.controller_switcher_client.switch_controller("cartesian_impedance_controller")
robot.cartesian_controller_parameters_client.load_param_config(
    file_path="operational_space_controller.yaml"
)

# TODO: This is a hack to close and open the gripper
# ros2 launch franka_gripper gripper.launch.py robot_ip:=<fci-ip>
# to grip:
# ros2 action send_goal -f /franka_gripper/grasp franka_msgs/action/Grasp "{width: 0.01, speed: 0.05, force: 50, epsilon: {inner: 0.05, outer: 0.05}}"
# to stop:
# ros2 service call /franka_gripper/stop std_srvs/srv/Trigger {}
# to home:
# ros2 action send_goal /franka_gripper/homing franka_msgs/action/Homing {}

# %%
input("Press Enter to go to the pickup point... ")
robot.move_to(position=pickup_point, speed=0.15)
robot.wait_until_ready()
# %%
input("Press Enter to pick up the item... ")
next_point = np.array([0.45, 0.0, 0.18])
robot.move_to(position=next_point, speed=0.15)
robot.wait_until_ready()

