#!/usr/bin/bash

set -e

echo 'Updating packages...'
sudo yum update -y

echo 'Installing git...'
sudo yum install git -y

echo 'Installing tmux...'
sudo yum install tmux -y

echo 'Installing docker...'
sudo amazon-linux-extras install docker
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

echo 'Installing docker compose v2...'
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.2.2/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose

echo 'Reconnect to this ec2 and clone the repo'