# Rclone-Backupper
---
## Summary
This python script may be used to automate the process of backing up files, directories or MySQL/MariaDB databases with Rclone.
## Dependencies
- Your favorite Linux distrobution
- [Python](https://www.python.org/downloads/) ***3.11 or higher***
  - This likely is installed by default in your Linux distrobution 
- [Rclone](https://rclone.org/downloads/)
- (Optional) - Some form of [chronjob manager](https://github.com/cronie-crond/cronie), if you wish to automatically perform scheduled backups
# Notes
- The python script and config file must be located in the same directory
-  The python script must be run with sudo/as root