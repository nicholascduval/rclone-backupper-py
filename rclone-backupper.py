import datetime, tomllib,sys, os, subprocess

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

#Copy each MySQL/MariaDB database specified in the config file to the temporary directory
for x in config["dbs"]:
    subprocess.run(f"mysqldump --single-transaction -h {x[1]} -u {x[2]} -p\"{x[3]}\" {x[0]} > {config['tempdir']}/{x[0]}.sql", shell=True)

#Set the backup filename
backup_filename_joined = f"{config['backup_filename']} {datetime.datetime.now().replace(microsecond=0)}.tgz"

# Compress the temporary directory into a tarball
subprocess.run(f"tar -czf \"/tmp/{backup_filename_joined}\" -P \"{config['tempdir']}\"", shell=True)

#Copy the tarball to the remote server
subprocess.run(f"sudo -u {config['rclone'][1]} rclone copy \"/tmp/{backup_filename_joined}\" {config['rclone'][0]}", shell=True)

#Delete the temporary directory and backup tarball
subprocess.run(f"rm -rf {config['tempdir']}", shell=True)
subprocess.run(f"rm -rf \"/tmp/{backup_filename_joined}\"", shell=True)

#Runs any commands specified by the user in the post_cmds list/array in the config file
for x in config["post_cmds"]:
    subprocess.run(x, shell=True)