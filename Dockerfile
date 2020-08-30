FROM python:3.8.5

# We specify our working directory
WORKDIR /youtube_playlists_follow_up
ADD . /youtube_playlists_follow_up

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_ENV development

# Expose the PORT 5000: incoming requests to our running Docker Container
EXPOSE 5000

CMD ["flask", "run"]