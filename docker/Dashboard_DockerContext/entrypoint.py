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
#                "python", 
#                "main.py", 
                "bokeh",
                "serve",
                "main.py",
                "/Input/bokeh_config.json"
                ]
        )

json_config=os.path.join('/Input', 'bokeh_config.json')
with open(json_config) as f: 
   params = json.load(f)

