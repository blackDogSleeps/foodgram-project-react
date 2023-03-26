id=$(sudo docker container ls | grep "^.* \<p" | cut -c 1-12)
sudo docker exec -it $id sh
