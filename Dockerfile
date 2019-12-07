FROM python:3.7-slim
#add a non-root user
RUN useradd -m "docker-user"
#change to user dir
WORKDIR /home/docker-user
#copy required files
COPY ["app.py", "wsgi.py", "functions.py", "requirements.txt", "./"]
#install required packages into home dir
RUN pip install -r "requirements.txt"
#change to non-root user
USER docker-user
#listen port for gunicorn
ENV PORT=8080
#run gunicorn
CMD ["gunicorn", "wsgi:app"]
