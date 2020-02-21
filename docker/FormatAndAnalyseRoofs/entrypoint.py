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
   output_dir = params["dir"]["output"]
   target_output_dir = os.path.join("/Output", output_dir)
for file in os.listdir(output_dir):
   print ("FILE", file)
#   target_name = os.path.join(target_output_dir, file)
#   shutil.copyfile(file, target_name)   
#shutil.rmtree(target_output_dir)
#shutil.copytree(output_dir, "/Output")
print ("TARGET", target_output_dir)