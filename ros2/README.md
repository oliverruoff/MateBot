# ROS

## Docker

- Using docker image: humble desktop jammy
    - humble -> ro2 distribution
    - desktop -> for graphics
    - jammy -> arm architecture (raspberry)

### Setup

- Install Docker:
    - curl -fsSL https://get.docker.com -o get-docker.sh
    - chmod +x get-docker.sh 
    - ./get-docker.sh
    - sudo usermod -aG docker pi(user)
    - sudo systemctl unmask docker
    - sudo chmod 666 /var/run/docker.sock
    - pip3 -v install docker-compose
    - sudo systemctl start docker
    - reboot now

### Run

- Run command:
```bash
docker run -it --net=host \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --privileged -v /dev/bus/usb:/dev/bus/usb \
    matebot:ros
```

## Run using docker-compose

- docker-compose build --no-cache
- docker-compose up -d
- docker exec -it f2b bash

## Run using docker command:

- docker run -it --net=host --device=/dev/ttyUSB0  imageName bash

## Run lidar node in docker

- ros2 launch ldlidar_ros2 ld19.launch.py

## Run ROS2 on windows

- Start "x64 Native Tools Command Prompt for VS 2019"  as admin
- paste:
```:: activate the ROS 2 environment
c:\opt\ros\foxy\x64\setup.bat

:: activate the Gazebo simulation environment
c:\opt\ros\foxy\x64\share\gazebo\setup.bat
set "SDF_PATH=c:\opt\ros\foxy\x64\share\sdformat\1.6"
```

- run rviz2: ros2 run rviz2 rviz2