id=$(sudo docker container ls | grep "^.* \<b" | cut -c 1-12)
sudo docker exec -it $id bash
