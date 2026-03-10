# Contact Decomposition Controller

![Hybrid Intelligent Experimental Robotics Lab logo](docs/assets/header.png)

## Contents
- [About](#about)
- [Docker Container Installation](docs/installation.md)
- [Run Examples](#run-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About
The **crisp_contact_decomposition** repository extends the [CRISP ROS2 controllers](https://github.com/utiasDSL/crisp_controllers) to a task-space hybrid control formulation that decomposes _SE(3)_ into independant pose-controlled and wrench-controlled subspaces, allowing for simultaneous position and force control in real time. This controller is compatible with ROS2, and is experimentally verified on hardware via the Franka Research 3 manipulator arm.

<div align="center">
  <video src="docs/assets/force_position_control_demo.mp4" autoplay loop muted style="max-width: 50%;"></video>
</div>

All work supported by the **Hybrid Intelligent Experimental Robotics Lab** at North Carolina State University. **[Visit the HIER Lab website](https://hier-robotics.github.io/).**


### Features

- An exposed `selection_vector` interface and correspondingly modified `crisp_py` publisher for control over task-force decomposition
- Slight performance enhancements to the original `cartesian_controller`

## Run Examples

### Franka arm operational space control
This demonstration is a direct application of the **CRISP OSC controller** and a good starting point for verifying everything works correctly.

After [installing the docker container](docs/installation.md):

  1. **Ensure FCI is enabled**
      We recommend running the `communication_test` before running the example for the first time.
      
      ```bash
      communication_test <robot-ip>
      ```

  2. **Start the controllers**
      In a seperate terminal, start the CRISP cartesian controller and franka gripper node
      ```bash
      cd /ros2_ws/ && source install/setup.bash
      export ROBOT_IP=<your robot ip address>
      ros2 launch contact_decomp_demos franka.launch.py robot_ip:=$ROBOT_IP & ros2 launch franka_gripper gripper.launch.py robot_ip:=$ROBOT_IP
      ```
      In the future, these will likely be launched from the same file. The gripper launch configuration will depend on the specific gripper connected to the arm.
    
  3. **Run the operational space control demo**
      In the original terminal (with .venv activated), run the demo.
      ```bash
      cd /ros2_ws/src/contact_decomp_demos/examples/
      python3 01_figure_eight_osc.py
      ```

## Troubleshooting
### libfranka issues

If you encounter libfranka issues, it is recommended to set up this package in isolation to verify it works independantly of this project. Please refer to the [libfranka installation instructions](https://github.com/frankarobotics/libfranka)

A real-time kernel is essential to ensure proper communication and to prevent timeout issues. For guidance on setting up a real-time kernel, please refer to the [Franka installation documentation](https://frankarobotics.github.io/docs/installation_linux.html#setting-up-the-real-time-kernel).

## Contributing

Contributions are welcome! Please fork this repository and create a pull request with your changes.

## License

All packages of crisp_contact_decomposition are licensed under the Apache 2.0 license.

## Contact

For questions or support, please open an issue on the [GitHub Issues](https://github.com/dmalexa5/crisp_contact_decomposition/issues) page.

Or, contact me at dmalexa5@ncsu.edu.

