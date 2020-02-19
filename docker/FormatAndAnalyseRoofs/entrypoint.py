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
                "python", 
                "get_analysed_roofs.py", 
                "/Input/config.json"
                ]
        )

json_config=os.path.join('/Input', 'config.json')
with open(json_config) as f: 
   params = json.load(f)
   output_file = params["dir"]["output"]
   target_output_file = os.path.join('/Output', output_file)
if os.path.isfile(output_file):
   shutil.copyfile(output_file, target_output_file)
