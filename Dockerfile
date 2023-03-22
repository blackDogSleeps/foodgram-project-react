FROM python:3.7-slim
WORKDIR /foodgram/
COPY . .
WORKDIR /foodgram/backend/
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "--bind", "0:8000", "foodgram.wsgi:application"]