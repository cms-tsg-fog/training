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


on tab 0 you should see the RateMon API server running.