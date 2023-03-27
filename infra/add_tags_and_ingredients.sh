id=$(sudo docker container ls | grep -E -i "^.* \<b" | cut -c 1-12)
sudo docker exec -it $id python manage.py add_tags_and_ingredients
