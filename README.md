> ***GeoDecision => Decision-making tools for urban management***

## Presentation
> ***Note** => This package is mainly use - for now - through [dockers](https://github.com/VCityTeam/UD-geodecision-docker)*

> ***TODO***

## Installation
### Warnings/Disclaimer
> ***/!\ Please read carefully these warnings related to spatial libraries installation***

Our package requires libraries with **spatial functionality** such as [GeoPandas](https://geopandas.org). Such libraries depends on on open source libraries ([GEOS](https://geos.osgeo.org/), [GDAL](https://www.gdal.org/), [PROJ](https://proj.org/)). As written in GeoPandas "*Those **base C libraries can sometimes be a challenge to install**. [...] So depending on your platform, you might need to compile and install their C dependencies manually. [...]. Using conda [...] avoids the need to compile the dependencies yourself.*".

If you want to read more about it, you may want to read the [GeoPandas installation warnings](https://geopandas.org/install.html#installation) and the [blog article on differences between conda and pip](https://www.anaconda.com/understanding-conda-and-pip/). You can also have a look on the table below (*from the just quoted blog article*)

|                       | conda                   | pip                             |
|-----------------------|-------------------------|---------------------------------|
| manages               | binaries                | wheel or source                 |
| can require compilers | no                      | yes                             |
| package types         | any                     | Python-only                     |
| create environment    | yes, built-in           | no, requires virtualenv or venv |
| **dependency checks** | **yes**                 | **no**                          |
| package sources       | Anaconda repo and cloud | PyPI                            |

Regarding these warnings and for **purposes of stability and multi-platform installations**, we choose to use [Conda](https://docs.conda.io/projects/conda/en/latest/) - *an open-source package management system and environment management system* - to install and work with our package. **We use pip - *only through conda* - for specific packages** (*that does not exist on [Anaconda](https://www.anaconda.com/) repo and cloud*). Conda is used massively now and especially in the **data science**, machine learning and AI domains (*it includes most of useful packages such as NumPy, Pandas, ...*) and for **visualization**.

We choose to install it through the creation of a **conda virtual environment** that install and contains all the **required libraries as well as our own package**.

### How to
#### Install geodecision environment (*containing geodecision package*)
1. Get & install conda:
    * [Miniconda](https://docs.conda.io/en/latest/miniconda.html) *=> minimal package*
    * [Anaconda](https://www.anaconda.com/distribution/) *=> includes graphical interface and other tools*
2. Clone or download this repository
3. Open a Command Line Interface inside the cloned repository
4. Install the environment and GeoDecision from the environment file:
    ```bash
    conda env create -f ./geodecision/env.yml
    ```

#### Use it
1. Once installation done, to use our package, activate the virtual environment:
    ```bash
    conda activate geodecision
    ```
2. You can use your IDE, Jupyter notebooks, *etc* ... inside this environnement via Anaconda tools or your favorite tools. You, of course, have to install these tools within this environment or connect them to it.

#### Future developments
We will certainly, for the future releases, develop a Conda package to make installation of our package simpler. But our package is still on a beta version and the [build of a Conda package](https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs.html) from a local package may require some time and improvements. If we want to build a pip install ready package, it will demand to make detailed instructions for each OS to avoid spatial dependencies installation problems (*it could be really difficult regarding the OS and the existing environment*).  

### Architecture
#### Python geodecision module and sub-modules
```
geodecision/
├── accessibility
│   ├── accessibility.py
│   ├── __init__.py
│   ├── isochrone.py
│   └── schema.py
├── bokeh_snippets
│   ├── bokeh_snippets.py
│   └── __init__.py
├── citygml
│   ├── analyseroofs.py
│   ├── categories.py
│   ├── constants.py
│   └── __init__.py
├── classification
│   ├── classification.py
│   ├── constants_vars.py
│   └── __init__.py
├── cli.py
├── geodecision.py
├── graph
│   ├── connectpoints.py
│   ├── __init__.py
│   ├── splittednodes.py
│   └── utils.py
├── __init__.py
├── logger
│   ├── __init__.py
│   └── logger.py
├── osmquery
│   ├── __init__.py
│   └── methods.py
└── spatialops
    ├── __init__.py
    └── operations.py
```

## Features
> ***TODO***

#### *To know more*
* [Manage conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#)
* [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) to easily create Python packages. *The package was created with Cookiecutter and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)*.
