sudo apt update
sudo apt install docker -Y

docker run -it -p 8080:8080 --name nudenet notaitech/nudenet:classifier
