import tomllib,sys, os, subprocess

#Finds the directory with the script and the config file
root_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
config_path=os.path.join(root_dir, "config.toml")

#Loads the config file, parses it with tomllib, and returns a dict with the values from the config file
with open(config_path, mode="rb") as config_file:
    config = tomllib.load(config_file)

#Runs any commands specified by the user in the pre_cmds list/array in the config file
for x in config["pre_cmds"]:             
    subprocess.run(x, shell=True)      

#Delete previous backup's temporary files (If they exist, which they shouldn't)
subprocess.run(f"rm -rf {config['tempdir']}", shell=True)

#Copy each file/directory specified in the config file to the temporary directory
for x in config["dirs"]:
    subprocess.run(f"cp -r {x} {config['tempdir']}", shell=True)



