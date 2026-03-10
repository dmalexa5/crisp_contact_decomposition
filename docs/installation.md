

## Docker Container Installation

([back to main](/README.md)) 

The **crisp_contact_decomposition** package includes a `Dockerfile` and a `docker-compose.yml`, which allows you to use crisp_contact_decomposition packages without manually installing **ROS 2**. Also, support for Dev Containers in Visual Studio Code is provided.

For detailed instructions, on preparing VSCode to use the `.devcontainer` follow the setup guide from [VSCode devcontainer_setup](https://code.visualstudio.com/docs/devcontainers/tutorial). These installation instruction were [adapted from franka_ros2](https://github.com/frankarobotics/franka_ros2/tree/humble?tab=readme-ov-file#local-machine-installation).

## Clone the repository

    ```bash
    git clone https://github.com/dmalexa5/crisp_contact_decomposition.git
    cd crisp_contact_decomposition
    ```
Next, build the docker container.

## Option A: using Docker Compose (recommended)

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

## Option B: using Dev Containers in Visual Studio Code

  2. **Open Visual Studio Code ...**

        Then, open folder  `crisp_contact_decomposition`

  3. **Choose `Reopen in container` when prompted.**

      The container will be built automatically, as required.

  4. **Clone the latests dependencies:**
      ```bash
      vcs import src < dependency.repos --recursive --skip-existing
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