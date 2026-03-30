"""Simple example using dual arm setup.

Note: for a better dual arm teleop setup, it would be better to simply map the /left/joint_states
to the /right/joints_states. But this setup is a bit easier to understand and play with.
"""

# %%
import time
from pathlib import Path

from crisp_py.robot import make_robot

# %%
CONFIG_DIR = Path(__file__).resolve().parents[1] / "config" / "teleop"
LEADER_TELEOP_CONFIG = CONFIG_DIR / "leader_teleop.yaml"
FOLLOWER_TELEOP_CONFIG = CONFIG_DIR / "follower_teleop.yaml"

left_arm = make_robot("fr3", namespace="leader")
right_arm = make_robot("fr3", namespace="follower")
left_arm.wait_until_ready()
right_arm.wait_until_ready()

# %%
print("Going to home position...")
left_arm.home(blocking=False)
right_arm.home(blocking=True)

# %%
left_arm.controller_switcher_client.switch_controller("cartesian_impedance_controller")
right_arm.controller_switcher_client.switch_controller("cartesian_impedance_controller")

left_arm.cartesian_controller_parameters_client.load_param_config(
    file_path=LEADER_TELEOP_CONFIG
)
right_arm.cartesian_controller_parameters_client.load_param_config(
    file_path=FOLLOWER_TELEOP_CONFIG
)


# %%
def sync(left_arm, right_arm):
    right_arm.set_target(pose=left_arm.end_effector_pose)
    right_arm.set_target_joint(left_arm.joint_values)


right_arm.node.create_timer(1.0 / 100.0, lambda: sync(left_arm, right_arm))

try:
    while True:
        print(f"Left arm joint values: {left_arm.joint_values}")
        print(f"Right arm joint values: {right_arm.joint_values}")
        print("-" * 40)
        time.sleep(1.0)
except KeyboardInterrupt:
    print("User exits teleop...")
finally:
    print("Going to home position...")
    left_arm.home()
    right_arm.home()
    left_arm.shutdown()
    right_arm.shutdown()
