# shutdown_script
Python script to automatically shut down the cluster during the night


# Install
To install the script, just clone the repo on a management 
node and create a cron job like here:
```
crontab -e
```


Insert this (--start -> explicitly start the node, 
otherwise a 'Press power button' command is sent.
```
0 7 * * * /path/to/script/shutdown.py --start
0 20 * * * /path/to/script/shutdown.py
```
