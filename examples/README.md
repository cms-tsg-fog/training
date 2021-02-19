# Example of using the RateMon tools

This directory contains example code for using the RateMon tools.

## Example of using the API

The `call_api.py` script is an example of using the `ratemon` API with a short python script.

First, set up the environment:
```
conda create --name example-env python=3.7.9
conda activate example-env
python -m pip install requests
python -m pip install requests[socks]
conda install root -c conda-forge
```
