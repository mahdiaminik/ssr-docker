#!/bin/bash

containers=$(docker ps -aq)
# loop through all containers
for container in $containers
do
  name=$(docker inspect $container | grep Name | head -n 1)
  users=$(docker exec -it $container sh -c 'netstat -n | grep :8388 | grep ESTABLISHED | wc -l')
  echo $name :  $users
done
