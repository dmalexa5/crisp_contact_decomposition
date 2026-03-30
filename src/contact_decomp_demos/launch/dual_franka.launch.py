from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def include_franka_arm(namespace, robot_ip, robot_type, load_gripper, use_fake_hardware, fake_sensor_commands, use_rviz):
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("contact_decomp_demos"),
                        "launch",
                        "franka.launch.py",
                    ]
                )
            ]
        ),
        launch_arguments={
            "robot_ip": robot_ip,
            "namespace": namespace,
            "robot_type": robot_type,
            "load_gripper": load_gripper,
            "use_fake_hardware": use_fake_hardware,
            "fake_sensor_commands": fake_sensor_commands,
            "use_rviz": use_rviz,
        }.items(),
    )


def generate_launch_description():
    leader_namespace = LaunchConfiguration("leader_namespace")
    leader_ip = LaunchConfiguration("leader_ip")
    follower_namespace = LaunchConfiguration("follower_namespace")
    follower_ip = LaunchConfiguration("follower_ip")
    robot_type = LaunchConfiguration("robot_type")
    load_gripper = LaunchConfiguration("load_gripper")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    fake_sensor_commands = LaunchConfiguration("fake_sensor_commands")
    use_rviz = LaunchConfiguration("use_rviz")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "leader_namespace",
                default_value="leader",
                description="Namespace for the leader arm.",
            ),
            DeclareLaunchArgument(
                "leader_ip",
                default_value="192.168.1.15",
                description="Hostname or IP address of the leader robot.",
            ),
            DeclareLaunchArgument(
                "follower_namespace",
                default_value="follower",
                description="Namespace for the follower arm.",
            ),
            DeclareLaunchArgument(
                "follower_ip",
                default_value="192.168.1.11",
                description="Hostname or IP address of the follower robot.",
            ),
            DeclareLaunchArgument(
                "robot_type",
                default_value="fr3",
                description="ID of the type of arm used. Supported values: fer, fr3, fp3",
            ),
            DeclareLaunchArgument(
                "load_gripper",
                default_value="true",
                description="Use Franka Gripper as an end-effector.",
            ),
            DeclareLaunchArgument(
                "use_fake_hardware",
                default_value="false",
                description="Use fake hardware.",
            ),
            DeclareLaunchArgument(
                "fake_sensor_commands",
                default_value="false",
                description="Fake sensor commands. Only valid when use_fake_hardware is true.",
            ),
            DeclareLaunchArgument(
                "use_rviz",
                default_value="false",
                description="Visualize the robots in Rviz.",
            ),
            include_franka_arm(
                leader_namespace,
                leader_ip,
                robot_type,
                load_gripper,
                use_fake_hardware,
                fake_sensor_commands,
                use_rviz,
            ),
            include_franka_arm(
                follower_namespace,
                follower_ip,
                robot_type,
                load_gripper,
                use_fake_hardware,
                fake_sensor_commands,
                use_rviz,
            ),
        ]
    )
