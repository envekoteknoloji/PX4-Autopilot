#!/bin/bash

xhost +local:

sudo docker run \
    --name px4_dev_container \
    --privileged \
    --net=host \
    --ipc=host \
    --shm-size=4gb \
    --gpus all \
    -it --rm \
    -v ./:/home/user/workspace/PX4-Autopilot \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    px4_image
