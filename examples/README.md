# Example of using the RateMon tools

This directory contains example code for using the RateMon tools.

## Example of using the API

The `call_api.py` script is an example of using the `ratemon` API with a short python script.

First, set up the environment with the necessary requirements:
```
conda create --name example-env python=3.7.9
conda activate example-env
python -m pip install requests
python -m pip install requests[socks]
conda install root -c conda-forge
```
Next, in the `PROXIES` dictionary in  `call_api.py`, fill in the appropriate `host` and `port`. Now you should be able to run `call_api.py`. The script expects a run number to be passed as a command line argument, so you can run the script e.g. like this:
```
python call_api.py 305112
```
