# Get Miniconda (Anaconda Python) from Docker Hub
# (https://hub.docker.com/r/continuumio/miniconda3)

FROM continuumio/miniconda3

# Create conda virtual environment
# (see:
#     - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file
#     - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually
#     - https://pythonspeed.com/articles/activate-conda-dockerfile/)

RUN apt-get install unzip
COPY env.yml .
RUN conda env create -f env.yml
#Get the Dashboard files on NextCloud, donwload them, unzip them into data
RUN mkdir data
RUN wget https://box.liris.cnrs.fr/s/Z9GKRqFP6rw9D9F/download && unzip download -d /data && rm download


# The code to run when container is started:
COPY geodecision .
COPY main.py .
COPY constants.py .
COPY entrypoint.py .
COPY background.geojson .
COPY bokeh_config.json .
#ENTRYPOINT ["python", "/entrypoint.py"]
CMD ["bokeh", "serve","main.py", "--args", "bokeh_config.json"]
#RUN bokeh serve main.py --args bokeh_config.json
