import subprocess
import json
import os
import shutil


input_config = "/Input/bokeh_config.json"

if os.path.isfile(input_config):
    subprocess.call(
            [
                    "conda", 
                    "run", 
                    "-n", 
                    "geodecision",
                    "bokeh",
                    "serve",
                    "dashboard",
                    "--args",
                    input_config
                    ]
            )
else:
    raise FileNotFoundError(
            "ERROR: Please check if {} exists".format(input_config)
            )