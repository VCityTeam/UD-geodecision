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
#                "--show",
#                "--allow-websocket-origin=localhost:5006",
                "dashboard",
                "--args",
                "/Input/bokeh_config.json"
                ]
        )
#print ("YOUPI")
#json_config=os.path.join('/Input', 'bokeh_config.json')
#with open(json_config) as f: 
#   params = json.load(f)
#   print ("PARAMS", params)

