sudo docker-compose down
sudo docker system prune -af
sudo docker volume rm infra_back_foodgram_database infra_back_media_value infra_back_static_value
sudo docker system df
sudo docker volume ls
