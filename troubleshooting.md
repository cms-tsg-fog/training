## Environmental Variable Error

How to fix is your traceback while running the ratemon code contains statements like this:

```bash
Could not find platform independent libraries <prefix>
Could not find platform dependent libraries <exec_prefix>
Consider setting $PYTHONHOME to <prefix>[:<exec_prefix>]

FileNotFoundError: [Errno 2] No such file or directory: 'ssocookies.txt'
```

The RateMon code is designed to be run on lxplus outside of a CMSSW environment. Running in other setups can cause environmental variables to set to bad values, which produce errors shown above. If you see these, try running on lxplus if you are not or make sure you do not do a cmsenv command before running the code.