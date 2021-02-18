# Connecting to a CERN OpenStack VM running the RateMon API

Set up ssh to use the necessary private key.

`~/.ssh/config`:

```
Host $HOSTNAME
  Hostname $HOSTNAME.cern.ch
  IdentityFile ~/.ssh/$PRIVATEKEY.pem
  User root
```

To login, run `ssh $HOSTNAME.cern.ch`.

If you're outside CERN, run this commands on LXPLUS or set up a ssh tunnel.

## SSH Tunnel

Set up a ssh tunnel trough LXPLUS:
```
ssh -D 1337 -q -N -f -C lxplus.cern.ch
```

Install `proxychains` and then edit `/etc/proxychains.conf` as follows:

```
# Strict - Each connection will be done via chained proxies
strict_chain
# Resolve DNS trough the proxy
proxy_dns[ProxyList]
# localhost SSH tunnel
socks5  127.0.0.1 1337
```

Now, you can prepend `proxychains` to any command to run it trough the ssh tunnel.

On Firefox/Chrome, install [FoxyProxy](https://addons.mozilla.org/it/firefox/addon/foxyproxy-standard/) and set up a SOCKS5 proxy on port `1337` and host `localhost` (or `0.0.0.0`) to browse as you were inside the CERN network (necessary to access anything served by CERN OpenStack machines).


### Tmux

Once you're logged in, run `tmux attach -t 0` to attach to the tmux session (keep shells running).

Once you're inside tmux:

- <kbd>CTRL</kbd>+<kbd>S</kbd> then <kbd>D</kbd> to detach and go back to the normal shell
- <kbd>CTRL</kbd>+<kbd>S</kbd> then <kbd>$NUMBER</kbd> to go to $NUMBER tab
- <kbd>CTRL</kbd>+<kbd>S</kbd> then <kbd>N</kbd> to create a new tab

On tab 0 you should see the RateMon API server running. If you try `tmux attach -t 0` and get `no sessions`, then you can start a new one by running just `tmux`. If you want to kill the session, run `tmux kill-session -t 0` from the normal shell.

### NGINX

To check what is happening with `nginx`, you can run `systemctl status nginx`. If it is green and shows "running" then it is functioning properly. To start or to stop:
- `systemctl start nginx`
- `systemctl stop nginx`


## When things go wrong

- If you try to view the API from your browser (at `http://ater.cern.ch/api/v1/ui/`) and see `"This site can't be reached The webpage at http://ater.cern.ch/api/v1/ui/ might be temporarily down or may have moved permanently to a new address"`, then probably it needs to be restarted. To restart, start `nginx`, and then run `server.py` inside of a `tmux` session, e.g.:
  ```
  systemctl start nginx
  cd ratemon/ratemon
  tmux
  python3 server.py
  ```
- If you try to view the API from your browser and see a 502 ("Bad Gateway") error, then probably main web server (`nginx`) is active but it cannot find the configured applicaiton to show you (in this case the ratemon API). To resolve this issue, first verify that `nginx` is running properly (with `systemctl status nginx`), then attach to the `tmux` session (or start a new one if necessary), and simply restart `server.py`.

