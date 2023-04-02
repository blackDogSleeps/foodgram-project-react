cp ../data/NotoSerif-Regular.ttf /usr/local/lib/python3.7/site-packages/reportlab/fonts
python manage.py migrate
python manage.py collectstatic
# python manage.py add_tags_and_ingredients
python manage.py loaddata fixtures.json

# none
