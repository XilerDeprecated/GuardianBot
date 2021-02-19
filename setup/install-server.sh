sudo apt update
sudo apt install docker -Y

docker run -it -p8080:8080 notaitech/nudenet:classifier
