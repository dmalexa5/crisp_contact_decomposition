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

print(robot.end_effector_pose)
print(robot.joint_values)

# Parameters for pickup location
pickup_point = np.array([0.45, 0.0, 0.17])
ctrl_freq = 50.0

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
input("Press Enter to run the demonstration... ")
time.sleep(3.0)
# Parameters
start = pickup_point.copy()[0:3]
end   = start + np.array([0.0, -0.20, 0.0])  # Move left by 20 cm
duration = 10.0        # seconds
ctrl_freq = 50.0       # Hz
settle_time = 1.0       # seconds

ee_poses = []
target_poses = []
ts = []

print("Starting linear trajectory...")

rate = robot.node.create_rate(ctrl_freq)
dt = 1.0 / ctrl_freq

# Keep current orientation, only change position
target_pose = robot.end_effector_pose.copy()
target_pose.position = start.copy()
robot.set_target(pose=target_pose)
robot.set_target_wrench(force=[0.0, 0.0, 0.0], torque=[0.0, 0.0, 0.0])

t = 0.0

# Linear interpolation loop
while t < duration:
    alpha = t / duration
    pos = (1.0 - alpha) * start + alpha * end

    target_pose.position = pos
    robot.set_target(pose=target_pose)
    robot.set_target_wrench(force=[0.0, 0.0, -15], torque=[0.0, 0.0, 0.65])

    rate.sleep()

    ee_poses.append(robot.end_effector_pose.copy())
    target_poses.append(robot._target_pose.copy())
    ts.append(t)

    t += dt

# Force exact final target
target_pose.position = end.copy()
robot.set_target_wrench(force=[0.0, 0.0, 0.0], torque=[0.0, 0.0, 0.0])
robot.set_target(pose=target_pose)

ee_poses.append(robot.end_effector_pose.copy())
target_poses.append(robot._target_pose.copy())
ts.append(duration)

# Settle period
t = duration
while t < duration + settle_time:
    rate.sleep()

    ee_poses.append(robot.end_effector_pose.copy())
    target_poses.append(robot._target_pose.copy())
    ts.append(t)

    t += dt

print("Done with linear trajectory.")