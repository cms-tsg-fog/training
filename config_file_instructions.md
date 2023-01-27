# Running ShiftMonitorTool with a config file
The `ShiftMonitorTool` script may be run with an option `--configFile`, which allows a JSON file to be passed to the `ShiftMonitorTool`. An example JSON file is included in the repository [here](https://gitlab.cern.ch/cms-tsg-fog/ratemon/-/blob/master/ratemon/ShiftMonitor_config.json). Any parameter (which is not on the protected list that is specified in the `ShiftMonitorNCR.py`) may be specified in the JSON file. When running with the configuration file option turned on, the code will check for updates to the configuration file each time the `runLoop()` is called (i.e. every 30s), and if there has been an update to the configuration file since the last check, the new values for the specified parameters will be applied.

# Usage
Any variable in ShiftMonitorNCR.py of the form `self.variableName` can be changed in the config file (except variables in the proected list from ShiftMonitorNCR.py. 

To do this, add a variable to the json file using the following syntax: 
```
"variableName": variableValue,
```

For example, if you would like to change the default value of `self.maxCBR` to 10, you would add the following text to the config file: 
```
"maxCBR": 10,
```

# Testing in simulate mode
To test your config file, start running ShiftMonitorTool in simulate mode, and specify a config file using the following command: 
```
python3 ShiftMonitorTool.py --simulate=<runNumber> --configFile=<path_to_config.json>
```

While ShiftMonitorTool is running, in a separate terminal window, modify and save the config file. There will be a printout on the currently running ShiftMonitorTool terminal saying that a variable was changed. The old and new values of the variable will be printed out. 

# Current Usage at P5
The current version of ratemon deployed at P5 is running with a config file. 

The file is located on the machine `kvm-s3562-1-ip151-84`. The path to the config file is `/cmsnfsratemon/ratemon/.ShiftMonitor_config.json`. 

Assuming you have write permissions to this directory, this file can be edited and changes made to variables will be applied at the next RateMon query.

**Do not make changes to this config file before testing in simulate mode on your own copy of ratemon as described above.** 
