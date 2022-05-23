For information regarding autotests, see the readme in the /tests/README.md

1. Container for Jenkins: 
docker volume create jenkins
docker run --name jenkins -ti     -v jenkins:/var/jenkins_home     -p 127.0.0.1:8080:8080     jenkins/jenkins:lts
2. 