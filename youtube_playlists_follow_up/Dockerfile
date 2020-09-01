################# START NEW IMAGE: BASE LAYER #################

FROM python:3.8.5 as base

# We specify our working directory
RUN mkdir /work/
WORKDIR /work/

# We copy and run the requirements.txt file
COPY ./src/requirements.txt /work/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# We copy the content of the src folder
COPY ./src/ /work/

# We define the Flask app environment variable
ENV FLASK_APP=app.py

################# START NEW IMAGE: DEBUG #################

FROM base as debug

RUN pip install ptvsd

WORKDIR /work/
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0.0 -p 5000

################# START NEW IMAGE: PRODUCTION #################
FROM base as prod

RUN mkdir /work/
WORKDIR /work/

CMD flask run -h 0.0.0 -p 5000

