# ----------------------------
# Base image
# ----------------------------
FROM ubuntu:22.04

# ----------------------------
# Environment variables
# ----------------------------
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1
ENV NVIDIA_DRIVER_CAPABILITIES=all

# ----------------------------
# Install apt packages
# ----------------------------
RUN apt-get update
RUN apt-get install -y sudo
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y nano
RUN apt-get install -y htop
RUN apt-get install -y xdg-utils
RUN apt-get install -y libfuse2
RUN apt-get install -y locales
RUN apt-get install -y terminator
RUN apt-get install -y libxcb-xinerama0
RUN apt-get install -y libxkbcommon-x11-0
RUN apt-get install -y libxcb-cursor0
RUN apt-get install -y ca-certificates
RUN apt-get install -y build-essential
RUN apt-get install -y software-properties-common
RUN apt-get install -y python3-pip
RUN apt-get install -y libsdl-image1.2-dev
RUN apt-get install -y gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl
RUN rm -rf /var/lib/apt/lists/*

# ----------------------------
# Configure locales
# ----------------------------
RUN locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && \
    export LANG=en_US.UTF-8

# ----------------------------
# Git safety configuration
# ----------------------------
RUN git config --global --add safe.directory '*'

# ----------------------------
# Create workspace & copy PX4 setup files
# ----------------------------
RUN mkdir -p /home/user/workspace/setup
COPY Tools/setup/ubuntu.sh /home/user/workspace/setup/ubuntu.sh
COPY Tools/setup/requirements.txt /home/user/workspace/setup/requirements.txt

# ----------------------------
# Run PX4 setup script
# ----------------------------
RUN cd /home/user/workspace/setup && \
    chmod +x ubuntu.sh && \
    ./ubuntu.sh

# ----------------------------
# Install ROS2 Humble
# ----------------------------
RUN add-apt-repository universe
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y ros-humble-desktop
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN apt-get install -y python3-colcon-common-extensions
RUN echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc

# ----------------------------
# Install ROS2 Gazebo Bridge
# ----------------------------
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
RUN apt-get update
RUN apt-get install -y ros-humble-ros-gzharmonic
RUN apt-get install -y ros-humble-joint-state-publisher-gui

# ----------------------------
# Install VS Code
# ----------------------------
RUN wget https://vscode.download.prss.microsoft.com/dbazure/download/stable/863d2581ecda6849923a2118d93a088b0745d9d6/code_1.87.2-1709912201_amd64.deb
RUN dpkg -i code_1.87.2-1709912201_amd64.deb
RUN mkdir -p /home/user/vscode
RUN code --install-extension usernamehw.errorlens --no-sandbox --user-data-dir /home/user/vscode
RUN code --install-extension ms-python.python --no-sandbox --user-data-dir /home/user/vscode
RUN code --install-extension ms-vscode.cpptools --no-sandbox --user-data-dir /home/user/vscode
RUN code --install-extension twxs.cmake --no-sandbox --user-data-dir /home/user/vscode
RUN code --install-extension ms-vscode.cmake-tools --no-sandbox --user-data-dir /home/user/vscode
RUN code --install-extension github.vscode-pull-request-github --no-sandbox --user-data-dir /home/user/vscode

# ----------------------------
# Set environment variables
# ----------------------------
ENV PX4_GZ_MODELS=/home/user/workspace/PX4-Autopilot/Tools/simulation/gz/models
ENV PX4_GZ_WORLDS=/home/user/workspace/PX4-Autopilot/Tools/simulation/gz/worlds
ENV PX4_GZ_PLANT_MODELS=/home/user/workspace/PX4-Autopilot/Tools/simulation/gz/plants
ENV PX4_GZ_GROUNDPLANE_MODELS=/home/user/workspace/PX4-Autopilot/Tools/simulation/gz/terrains
ENV GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$PX4_GZ_MODELS:$PX4_GZ_PLANT_MODELS:$PX4_GZ_WORLDS:$PX4_GZ_GROUNDPLANE_MODELS
ENV PX4_GZ_MODEL_POSE="0,0,0.5"
ENV GZ_IP=127.0.0.1

# ----------------------------
# Default container command
# ----------------------------
CMD bash -c "echo STARTING ROS2 GZ BRIDGE IMAGE NODE && \
    echo INITIALIZING... && \
    source /opt/ros/humble/setup.bash && \
    (ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:=home/user/workspace/PX4-Autopilot/rover-sim/bridge.yaml -p qos_overrides./tf_static.publisher.durability:=transient_local &) && \
    wait && \
    cd /home/user/workspace && \
    echo PRESS ENTER && \
    exec bash"

