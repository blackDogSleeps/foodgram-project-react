![BADGE](https://github.com/blackDogSleeps/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


# Foodgram
Учебный проект для размещения и обмена кулинарными рецептами. Можно подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», скачивать сводный список продуктов.

## Как запустить проект:
Клонировать репозиторий и перейти в директорию `foodgram-project-react/infra/`:
```
git clone git@github.com:blackDogSleeps/foodgram-project-react.git
cd foodgram-project-react/infra/
```

Собрать стек контейнеров с помощью скрипта:
```
bash start.sh
```

Скрипт соберет проект, сделает миграции, наполнит базу данных из файла `/backend/fixtures.json`

Если файл `fixtures.json` отстутствует или вам нужен чистый проект, удалите `fixtures.json` из директории `backend`, а из директории `infra` запустите скрипт:
```
bash add_tags_and_ingredients.sh
```


## Панель администратора
```
http://$host/admin
```



