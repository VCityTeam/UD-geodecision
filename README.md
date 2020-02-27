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

### Developer's information
#### About Cookiecutter (*create package*)
> [Complete guide](https://docs.python-guide.org/writing/structure/)

> To make license choice easier, check [choosealicense](http://choosealicense.com/)

##### Quick & easy way
* Use [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and one of their templates like [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
```
pip install -U cookiecutter
cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git
```

##### Documentation
> We use [Sphinx](http://www.sphinx-doc.org/) for documentation

###### A good structuration
Once you have put your modules into the generated structure, it is time to organise it in a pythonic way. Below is what you get when you use the [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage). In this example, you have a module named ```mymodule```.
```
 mymodule:
    |--- AUTHORS.rst
    |--- CONTRIBUTING.rst
    |--- HISTORY.rst
    |--- Makefile
    |--- MANIFEST.in
    |--- README.rst
    |--- requirements_dev.text
    |--- setup.cfg
    |--- setup.py
    |--- tox.ini
    |--- .editorconfig
    |--- .gitignore
    |--- .travis.yml
    |___ docs
    |    |--- authors.rst
    |    |--- conf.py
    |    |--- contributing.rst
    |    |--- history.rst
    |    |--- index.rst
    |    |--- installation.rst
    |    |--- make.bat
    |    |--- Makefile
    |    |--- modules.rst
    |    |--- readme.rst
    |    |--- usage.rst
    |___ mymodule:
    |    |--- cli.py
    |    |--- __init__.py
    |    |--- mymodule.py
    |___ tests
    |    |--- __init__.py
    |    |--- test_mymodule.py
    |___ .github
```

If you already have module and sub-modules, put them in:
```
mymodule
    |___ mymodule
```
Once done, don't forget to check if the ```import``` are done in the right way. Let's say you have this architecture;
```
mymodule
    |___ mymodule
         |--- cli.py
         |--- __init__.py
         |--- mymodule.py
         |___ submoduleA
         |    |--- __init__.py
         |    |--- submoduleAOne
         |    |--- submoduleATwo
         |___ submoduleB
              |--- __init__.py
              |--- submoduleBOne
              |--- submoduleBTwo
```
If you want ***class OneA***  from ```submoduleAOne``` and ***class TwoB*** from ```submoduleBTwo``` to be accessible from your module, you need to edit the ```__init__.py```:
```
mymodule
    |___ mymodule
         |--- __init__.py
```
You have to add these lines:
```python
from .submoduleA.submoduleAOne import OneA
from .submoduleB.submoduleBTwo import TwoB
```

If you want to import ***class OneB*** from ```submoduleBOne``` in ```submoduleATwo``` you need to add this line in ```submoduleATwo```:
```python
from ..submoduleB.submoduleBOne import OneB
```

###### Generate documentation with Sphinx
> ***/!\ If you use the [numpydoc docstrings](https://numpydoc.readthedocs.io/en/latest/format.html#), add the [napoleon sphinx extension](http://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) in ```conf.py```***:
```
mymodule:
   |___ docs
        |--- conf.py
```
```python
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.napoleon']
```

Then generate documentation with command lines. Start a command line inside ```docs``` repository:
```
sphinx-apidoc -f -o . ../mymodule/
```
It will generate a bunch of ***rst*** files. Then, to get ***html*** pages (*in a ```_build``` directory for example*):
```
cd ..
sphinx-build -b html docs/ _build/
```

#### *To know more*
* [Manage conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#)
* [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) to easily create Python packages. *The package was created with Cookiecutter and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)*.
