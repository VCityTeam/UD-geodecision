# Get Miniconda (Anaconda Python) from Docker Hub
# (https://hub.docker.com/r/continuumio/miniconda3)

FROM continuumio/miniconda3

# Create conda virtual environment
# (see:
#     - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file
#     - https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually
#     - https://pythonspeed.com/articles/activate-conda-dockerfile/)

# Install unzip to manage the files that will be downloaded
RUN apt-get install unzip

# Retrieve UD-geodecision's code (some git credentials are expected)
ARG git_token
RUN git clone https://$git_token@github.com/VCityTeam/UD-geodecision.git

# Create conda virtual environment and install geodecision
RUN conda env create -f ./UD-geodecision/geodecision/env.yml

# Copy necessary file to run the docker
COPY entrypoint.py .

# Add dashboard app directory
ADD dashboard ./dashboard

# Get the Dashboard files on NextCloud, download them, unzip them into data
RUN mkdir /dashboard/data
RUN wget https://box.liris.cnrs.fr/s/Z9GKRqFP6rw9D9F/download && unzip download -d /dashboard/data && rm download

# Run the entrypoint
ENTRYPOINT ["python", "/entrypoint.py"]
