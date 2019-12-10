FROM python:3.7-slim
#add a non-root user
RUN useradd -m "docker-user"
#change to user dir
WORKDIR /home/docker-user
#copy requirements file, don't copy other files yet so that the pip install doesn't get triggered after every change
COPY ["requirements.pip", "./"]
#install required packages into home dir
RUN pip install -r "requirements.pip"
#now copy required files
COPY ["app.py", "wsgi.py", "functions.py", "./"]
#change to non-root user
USER docker-user
#listen port for gunicorn
ENV PORT=8080
#run gunicorn
CMD ["gunicorn", "wsgi:app"]
