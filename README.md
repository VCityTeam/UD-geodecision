Geodecision is a Python package

## Disclaimer

## Installation
### Warnings/Disclaimer
> ***/!\ Please read carefully these warnings related to spatial libraries installation***

Our package requires libraries with spatial functionality such as [GeoPandas](https://geopandas.org). Such libraries depends on on open source libraries ([GEOS](https://geos.osgeo.org/), [GDAL](https://www.gdal.org/), [PROJ](https://proj.org/)). As written in GeoPandas "*Those base C libraries can sometimes be a challenge to install. [...] So depending on your platform, you might need to compile and install their C dependencies manually. [...]. Using conda [...] avoids the need to compile the dependencies yourself.*".

If you want to read more about it, you may want to read the [GeoPandas installation warnings](https://geopandas.org/install.html#installation) and the [blog article on differences between conda and pip](https://www.anaconda.com/understanding-conda-and-pip/). You can also have a look on the table below (*from the just quoted blog article*)

|                       | conda                   | pip                             |
|-----------------------|-------------------------|---------------------------------|
| manages               | binaries                | wheel or source                 |
| can require compilers | no                      | yes                             |
| package types         | any                     | Python-only                     |
| create environment    | yes, built-in           | no, requires virtualenv or venv |
| dependency checks     | yes                     | no                              |
| package sources       | Anaconda repo and cloud | PyPI                            |

Regarding these warnings and for purposes of stability and multi-platform installation, we choose to use [Conda](https://conda.io/en/latest/) to install and work with our package. We use pip - only through conda - for specific packages (*that does not exist on [Anaconda](https://www.anaconda.com/) repo and cloud*). Conda is used massively now and especially in the data science (*webmapping*) domains.

We choose to install it through the creation of a conda virtual environment that install and contains all the required libraries as well as our own package.

#### Future developments
We will certainly, for the future releases, develop a Conda package to make installation of our package simpler. But our package is still on a beta version and the [build of a Conda package](https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs.html) from a local package may require some time and improvements.   
