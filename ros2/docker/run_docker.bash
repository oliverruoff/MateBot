xhost local:root

XAUTH=/tmp/.docker.xauth

docker run -it \
    --name= matebot \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="XAUTHORITY=$XAUTH" \
    --net=host \
    --privileged \
    matebot:ros \
    bash