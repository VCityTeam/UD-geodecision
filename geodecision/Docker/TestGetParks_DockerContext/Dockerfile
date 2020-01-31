# Get Miniconda (Anaconda Python) from Docker Hub
# (https://hub.docker.com/r/continuumio/miniconda3)

FROM continuumio/miniconda3

# Create conda virtual environment
# (see:
#     - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file
#     - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually
#     - https://pythonspeed.com/articles/activate-conda-dockerfile/)

COPY env.yml .
RUN conda env create -f env.yml

# The code to run when container is started:

COPY run.py .
COPY entrypoint.py .
COPY methods.py .
ENTRYPOINT ["python", "/entrypoint.py"]
