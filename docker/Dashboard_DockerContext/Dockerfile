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

# The code to run when container is started:
COPY geodecision .
COPY entrypoint.py .
COPY background.geojson .
COPY bokeh_config.json .
ADD dashboard ./dashboard
#Get the Dashboard files on NextCloud, download them, unzip them into data
RUN mkdir /dashboard/data
RUN wget https://box.liris.cnrs.fr/s/Z9GKRqFP6rw9D9F/download && unzip download -d /dashboard/data && rm download
#EXPOSE 5006
ENTRYPOINT ["python", "/entrypoint.py"]
#CMD ["conda","run","-n","geodecision","bokeh","serve","--show","--allow-websocket-origin=localhost:5006","/dashboard", "--args", "/Input/bokeh_config.json"]
