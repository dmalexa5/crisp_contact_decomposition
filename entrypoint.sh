#!/bin/bash

# Clone dependencies into the workspace
vcs import /ros2_ws/src < /ros2_ws/src/dependency.repos --recursive --skip-existing

source /ros2_ws/.venv/bin/activate

exec "$@"