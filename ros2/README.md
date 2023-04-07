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

___________

- docker-compose build --no-cache
- docker-compose up -d
- docker exec -it f2b bash