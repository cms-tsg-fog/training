## Environmental Variable Error

How to fix is your traceback while running the ratemon code contains statements like this:

```bash
Could not find platform independent libraries <prefix>
Could not find platform dependent libraries <exec_prefix>
Consider setting $PYTHONHOME to <prefix>[:<exec_prefix>]

FileNotFoundError: [Errno 2] No such file or directory: 'ssocookies.txt'
```

The RateMon code is designed to be run on lxplus outside of a CMSSW environment. Running in other setups can cause environmental variables to set to bad values, which produce errors shown above. If you see these, try running on lxplus if you are not or make sure you do not do a cmsenv command before running the code.

## Transient Query Error

```bash
File "/usr/lib/python3.6/site-packages/requests/models.py", line 885, in json
    return complexjson.loads(self.text, **kwargs)
  File "/usr/lib64/python3.6/json/__init__.py", line 354, in loads
    return _default_decoder.decode(s)
  File "/usr/lib64/python3.6/json/decoder.py", line 339, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib64/python3.6/json/decoder.py", line 357, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

If this is in your stack trace, the code encountered a transient error that is caused by the OMS query failing. Re-running the code in the same state should fix the problem.