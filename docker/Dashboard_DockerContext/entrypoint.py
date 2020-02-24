import subprocess
import json
import os
import shutil


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
                "/Input/bokeh_config.json"
                ]
        )