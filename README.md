![Hybrid Intelligent Experimental Robotics Lab logo](docs/assets/logo_5.png)

**[Visit the HIER Lab website](https://hier-robotics.github.io/)**

## Contents
- [About](#about)
- [Docker Container Installation](#docker-container-installation)
- [Run Examples](#run-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About
The **crisp_contact_decomposition** repository extends the [CRISP ROS2 controllers](https://github.com/utiasDSL/crisp_controllers) to a task-space hybrid control formulation that decomposes _SE(3)_ into independant pose-controlled and wrench-controlled subspaces, allowing for simultaneous position and force control in real time.

This controller is compatible with ROS2, is experimentally verified on hardware via the Franka Research 3 manipulator arm, and is tested in simulation. 

<!-- TODO: add manipulator simulation information -->

### Features

<!-- TODO: list contributions from this controller -->

## Docker Container Installation

([adapted from franka_ros2](https://github.com/frankarobotics/franka_ros2/tree/humble?tab=readme-ov-file#local-machine-installation))

The **crisp_contact_decomposition** package includes a `Dockerfile` and a `docker-compose.yml`, which allows you to use crisp_contact_decomposition packages without manually installing **ROS 2**. Also, support for Dev Containers in Visual Studio Code is provided.

For detailed instructions, on preparing VSCode to use the `.devcontainer` follow the setup guide from [VSCode devcontainer_setup](https://code.visualstudio.com/docs/devcontainers/tutorial).

1. **Clone the Repositories:**
    ```bash
    git clone https://github.com/dmalexa5/crisp_contact_decomposition.git
    cd crisp_contact_decomposition
    ```
Next, build the docker container.

### Option A: using Docker Compose (recommended)

You must have **docker engine** installed, **_not_** docker desktop. This will interfere with the container inheriting the `PREEMPT_RT` kernel neccessary to drive franka manipulators.

  1. **Save the current user id into a file:**
      ```bash
      echo -e "USER_UID=$(id -u $USER)\nUSER_GID=$(id -g $USER)" > .env
      ```
      It is needed to mount the folder from inside the Docker container.

  2. **Build the container:**
      ```bash
      docker compose build
      ```
  3. **Run the container:**
      ```bash
      docker compose up -d
      ```
  4. **Open a shell inside the container:**
      ```bash
      docker exec -it crisp_contact_decomposition /bin/bash
      ```
      or
      `Ctrl + Shift + P` > `Dev Containers: Attach to Running Container`
  5. **Clone the latests dependencies:**
      ```bash
      cd /ros2_ws
      vcs import src < dependency.repos --recursive --skip-existing
      ```
  6. **Build the workspace:**
      ```bash
      colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
      ```
> [!NOTE]
> This project is in rapid development. Warnings are expected, especially during the first build.

  7. **Source the built workspace:**
      ```bash
      source install/setup.bash
      ```

### Option B: using Dev Containers in Visual Studio Code

  2. **Open Visual Studio Code ...**

        Then, open folder  `crisp_contact_decomposition`

  3. **Choose `Reopen in container` when prompted.**

      The container will be built automatically, as required.

  4. **Clone the latests dependencies:**
      ```bash
      vcs import src < src/dependency.repos --recursive --skip-existing
      ```

  5. **Open a terminal and build the workspace:**
      ```bash
      colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
      ```
  6. **Source the built workspace environment:**
      ```bash
      source install/setup.bash
      ```

## Python environement setup

This package is set up to install `crisp_py` as an editable python package into a virtual environment that has access to system site packages.

  1. **Activate the virtual environment:**
      ```bash
      source /ros2_ws/.venv/bin/activate
      ```
  2. **Install crisp_py:**
      ```bash
      cd /ros2_ws/src/crisp_py/
      pip install -e .
      ```

## Run Examples

### Franka arm operational space control
This demonstration is a direct application of the CRISP OSC controller and a good starting point for verifying everything works correctly.

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
      In the future, these will likely be launched from the same file.
    
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

[def]: #docker-container-installation
