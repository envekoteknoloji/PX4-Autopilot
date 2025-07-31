from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    # Configure ROS nodes for launch
    # Necessary GZ - ROS2 bridge nodes are should be started before

    # Load the SDF file from "description" package
    # Write the model SDF file to /robot_description topic
    sdf_file  =  "/home/user/workspace/PX4-Autopilot/Tools/simulation/gz/models/b3rb/model.sdf"
    rviz_config_file = '/home/user/workspace/PX4-Autopilot/rover-sim/rviz_config.rviz'
    with open(sdf_file, 'r') as infp:
        robot_desc = infp.read()


    # Takes the description and joint angles as inputs and publishes the 3D poses of the robot links
    # This can't handle dynamic joints
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )

    # For dynamic joint states of the robot
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        arguments=[sdf_file],
        output=['screen'],
        parameters=[{'use_sim_time' : True}]
    )

    # Launch rviz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        condition=IfCondition(LaunchConfiguration('rviz')),
        parameters=[
            {'use_sim_time': True},
        ],
        arguments=['-d', rviz_config_file],
    )

    rviz_launch_arg = DeclareLaunchArgument(
        'rviz', default_value='true',
        description='Open RViz.'
    )

    # — New: publish a static identity transform body → odom —
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_body_to_odom',
        output='screen',
        # x y z yaw pitch roll frame_id child_frame_id
        arguments=[
            '0', '0', '0',   # zero translation
            '0', '0', '0',   # zero rotation (yaw, pitch, roll)
            'body', 'odom',  # parent frame, child frame
        ],
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription([
        rviz_launch_arg,
        rviz,
        robot_state_publisher,
        joint_state_publisher,
        static_tf,      # <-- added here
    ])
