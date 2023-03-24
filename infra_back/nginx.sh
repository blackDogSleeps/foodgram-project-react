id=$(sudo docker container ls | grep "^.* \<n" | cut -c 1-12)
sudo docker exec -it $id sh
