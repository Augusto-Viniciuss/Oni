from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    oni_gazebo_path = get_package_share_path("oni_gazebo")
    model_oni_path = oni_gazebo_path / "oni_description/oni.urdf.xacro"
    rviz_config_path = oni_gazebo_path / "rviz/config_oni.rviz"

    gui_arg = DeclareLaunchArgument(name="gui", default_value="false", choices=["true", "false"], description="Flag to enable joint_state_publisher_gui")
    model_arg = DeclareLaunchArgument(name="model", default_value=str(model_oni_path), description="Absolute path to robot urdf file")
    rviz_arg = DeclareLaunchArgument(name="rvizconfig", default_value=str(rviz_config_path), description="Absolute path to rviz config file")
    
    robot_description = ParameterValue(
   	 	Command(["xacro ", LaunchConfiguration("model")]) ,
      	value_type=str ,
    )
 
    robot_state_publisher_node = Node(
   	 	package= "robot_state_publisher" ,
   	 	executable= "robot_state_publisher" ,
   	 	name= "robot_state_publisher" ,
   	 	parameters= [{"robot_description" : robot_description}],
    )
 
    joint_state_publisher_node = Node(
   		package="joint_state_publisher",
   		executable="joint_state_publisher",
   		condition=UnlessCondition(LaunchConfiguration("gui"))
   	 )

    joint_state_publisher_gui_node = Node(
   		package="joint_state_publisher_gui",
   		executable="joint_state_publisher_gui",
  		condition=IfCondition(LaunchConfiguration("gui"))
   	 )
 
    rviz_node = Node(
   	 	package= "rviz2" ,
   	 	executable= "rviz2" ,
   	 	name= "rviz2" ,
   	 	output= "screen" ,
   	 	arguments=["-d", LaunchConfiguration("rvizconfig")] ,
    )
    
    gazebo_node = Node(
   	 	package= "gazebo_ros",
   	 	executable= "spawn_entity.py" ,
   	 	name= "oni_spawner" ,
   	 	output= "screen" ,
   	 	arguments= ["-topic", "/robot_description", "-entity", "oni", "-z", "0.03"]
    )

    return LaunchDescription([
   	 	gui_arg,
    	model_arg ,
   	 	rviz_arg ,
   	 	robot_state_publisher_node ,
   	 	joint_state_publisher_node ,
   	 	joint_state_publisher_gui_node ,
   	 	rviz_node ,
   	 	gazebo_node ,
    ])
