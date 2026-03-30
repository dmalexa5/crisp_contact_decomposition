#  Copyright (c) 2024 Franka Robotics GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    Shutdown,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def robot_description_dependent_nodes_spawner(
    context: LaunchContext
):
    robot_type = LaunchConfiguration("robot_type").perform(context)
    arm_prefix = LaunchConfiguration("arm_prefix").perform(context)
    namespace = LaunchConfiguration("namespace").perform(context)

    franka_xacro_filepath = os.path.join(
        get_package_share_directory('franka_description'),
        'robots',
        robot_type,
        robot_type + '.urdf.xacro'
    )

    robot_description = xacro.process_file(
        franka_xacro_filepath,
        mappings={
            "ros2_control": "true",
            "robot_type": robot_type,
            "robot_ip": LaunchConfiguration("robot_ip").perform(context),
            "hand": LaunchConfiguration("load_gripper").perform(context),
            "use_fake_hardware": LaunchConfiguration("use_fake_hardware").perform(context),
            "fake_sensor_commands": LaunchConfiguration("fake_sensor_commands").perform(context),
            "arm_prefix": arm_prefix,
            "namespace": LaunchConfiguration("namespace").perform(context),
        },
    ).toprettyxml(indent="  ")

    franka_controllers = PathJoinSubstitution(
        [
            FindPackageShare("contact_decomp_demos"),
            "config",
            "fr3",
            f"{arm_prefix}_controllers.yaml"
            if arm_prefix != ""
            else "controllers.yaml",
        ]
    )

    return [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            namespace=namespace,
            output="screen",
            parameters=[{"robot_description": robot_description}],
        ),
        Node(
            package="controller_manager",
            executable="ros2_control_node",
            namespace=namespace,
            parameters=[
                franka_controllers,
                {"robot_description": robot_description},
            ],
            remappings=[("joint_states", "franka/joint_states")],
            output={
                "stdout": "screen",
                "stderr": "screen",
            },
            on_exit=Shutdown(),
        ),
    ]


def generate_launch_description():
    robot_type_parameter_name = "robot_type"
    arm_prefix_parameter_name = "arm_prefix"
    robot_ip_parameter_name = "robot_ip"
    load_gripper_parameter_name = "load_gripper"
    use_fake_hardware_parameter_name = "use_fake_hardware"
    fake_sensor_commands_parameter_name = "fake_sensor_commands"
    use_rviz_parameter_name = "use_rviz"
    namespace_parameter_name = "namespace"

    robot_type = LaunchConfiguration(robot_type_parameter_name)
    arm_prefix = LaunchConfiguration(arm_prefix_parameter_name)
    robot_ip = LaunchConfiguration(robot_ip_parameter_name)
    load_gripper = LaunchConfiguration(load_gripper_parameter_name)
    use_fake_hardware = LaunchConfiguration(use_fake_hardware_parameter_name)
    fake_sensor_commands = LaunchConfiguration(fake_sensor_commands_parameter_name)
    use_rviz = LaunchConfiguration(use_rviz_parameter_name)
    namespace = LaunchConfiguration(namespace_parameter_name)

    rviz_file = os.path.join(
        get_package_share_directory("franka_description"),
        "rviz",
        "visualize_franka.rviz",
    )

    robot_description_dependent_nodes_spawner_opaque_function = OpaqueFunction(
        function=robot_description_dependent_nodes_spawner,
    )

    launch_description = LaunchDescription(
        [
            DeclareLaunchArgument(
                robot_ip_parameter_name,
                description="Hostname or IP address of the robot.",
            ),
            DeclareLaunchArgument(
                robot_type_parameter_name,
                default_value="fr3",
                description="ID of the type of arm used. Supported values: fer, fr3, fp3",
            ),
            DeclareLaunchArgument(
                use_rviz_parameter_name,
                default_value="false",
                description="Visualize the robot in Rviz",
            ),
            DeclareLaunchArgument(
                use_fake_hardware_parameter_name,
                default_value="false",
                description="Use fake hardware",
            ),
            DeclareLaunchArgument(
                fake_sensor_commands_parameter_name,
                default_value="false",
                description='Fake sensor commands. Only valid when "{}" is true'.format(
                    use_fake_hardware_parameter_name
                ),
            ),
            DeclareLaunchArgument(
                load_gripper_parameter_name,
                default_value="true",
                description="Use Franka Gripper as an end-effector, otherwise, the robot is loaded "
                "without an end-effector.",
            ),
            DeclareLaunchArgument(
                arm_prefix_parameter_name,
                default_value="",
                description="The prefix of the arm.",
            ),
            DeclareLaunchArgument(
                namespace_parameter_name,
                default_value="",
                description='Namespace for the robot. If not set, the robot will be launched in the root namespace.'),
            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
                namespace=namespace,
                parameters=[
                    {
                        "source_list": [
                            "franka/joint_states",
                            "franka_gripper/joint_states",
                        ],
                        "rate": 1000,
                    }
                ],
            ),
            robot_description_dependent_nodes_spawner_opaque_function,
            Node(
                package="controller_manager",
                executable="spawner",
                namespace=namespace,
                arguments=["joint_state_broadcaster"],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                namespace=namespace,
                arguments=["cartesian_impedance_controller", "--inactive"],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                namespace=namespace,
                arguments=["joint_trajectory_controller"],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                namespace=namespace,
                arguments=["twist_broadcaster"],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                namespace=namespace,
                arguments=["pose_broadcaster"],
                output="screen",
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [
                        PathJoinSubstitution(
                            [
                                FindPackageShare("franka_gripper"),
                                "launch",
                                "gripper.launch.py",
                            ]
                        )
                    ]
                ),
                launch_arguments={
                    robot_ip_parameter_name: robot_ip,
                    "robot_type": robot_type,
                    use_fake_hardware_parameter_name: use_fake_hardware,
                    namespace_parameter_name: namespace,
                }.items(),
                condition=IfCondition(load_gripper),
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["--display-config", rviz_file],
                condition=IfCondition(use_rviz),
            ),
        ]
    )

    return launch_description
