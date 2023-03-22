sudo docker-compose down
sudo docker system prune -af
sudo docker volume rm infra_foodgram_database infra_media_value infra_static_value
sudo docker system df
sudo docker volume ls
