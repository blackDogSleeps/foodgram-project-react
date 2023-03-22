import os
import re

DOCKER_ENV = ('DB_ENGINE=django.db.backends.postgresql\n'
              'DB_NAME=postgres\n'
              'POSTGRES_USER=postgres\n'
              'POSTGRES_PASSWORD=%tghy65tg\n'
              'DB_HOST=db\n'
              'DB_PORT=5432\n')

LOCAL_VENV = ('DB_ENGINE=django.db.backends.postgresql\n'
              'DB_NAME=foodgram\n'
              'POSTGRES_USER=foodgram_user\n'
              'POSTGRES_PASSWORD=%tghy65tg\n'
              'DB_HOST=localhost\n'
              'DB_PORT=5432\n')

os.chdir('foodgram/')
current_env = open('.env', encoding='UTF-8')
env_list = current_env.read().split('\n')
current_env.close()
postgres = len(re.findall('postgres', env_list[1]))
os.remove('.env')
os.remove('../../infra/.env')
new_env = open('.env', 'w', encoding='UTF-8')
new_env_two = open('../../infra/.env', 'w', encoding='UTF-8')

if postgres == 1:
    new_env.write(LOCAL_VENV)
    new_env_two.write(LOCAL_VENV)
    print(LOCAL_VENV)
else:
	new_env.write(DOCKER_ENV)
	new_env_two.write(DOCKER_ENV)
	print(DOCKER_ENV)

new_env.close()
new_env_two.close()
