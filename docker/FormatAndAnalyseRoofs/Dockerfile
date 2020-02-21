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
#Get the CityGML files on NextCloud, donwload them, unzip them into data
RUN mkdir data
RUN mkdir /data/outputs
#RUN wget https://box.liris.cnrs.fr/s/S6pxYb4kEmzCFgt/download && unzip download -d /data && rm download
RUN wget https://box.liris.cnrs.fr/s/RpLmwooKtXzSmCR/download && unzip download -d /data && rm download

# The code to run when container is started:
COPY geodecision .
COPY get_analysed_roofs.py .
COPY entrypoint.py .
ENTRYPOINT ["python", "/entrypoint.py"]
