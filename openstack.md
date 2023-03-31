# About the RateMon API

* Files that constitute the RateMon API:
    - [server.py](https://gitlab.cern.ch/cms-tsg-fog/ratemon/-/blob/master/ratemon/server.py): This is the script that is actually running on e.g. `ater`. It depends on `ratemon.yaml`. The [Connexion quickstart](https://connexion.readthedocs.io/en/latest/quickstart.html) documentation explains how this is set up.
    - [ratemon.yaml](https://gitlab.cern.ch/cms-tsg-fog/ratemon/-/blob/master/ratemon/api/ratemon.yaml): This yaml file defines the endpionts that the user (e.g. OMS) can point to. It depends on `app.py`. This [OpenAPI tutorial](https://idratherbewriting.com/learnapidoc/pubapis_openapi_tutorial_overview.html) explains how the yaml file is structured.
    - [app.py](https://gitlab.cern.ch/cms-tsg-fog/ratemon/-/blob/master/ratemon/app.py): This script imports `plotTriggerRates` and defines the functions that act as the link between the endpoints that the user (e.g. OMS) points to (which are defined in the yaml) and the underlying RateMon code. In other words, this script defines the functions that are "called" in the yaml file; these functions in app.py are essentially wrappers around RateMon functions.

* Slides explaining how the RateMon API is set up:
    - Presentation to OMS (Apr 27, 2021) [slides](https://indico.cern.ch/event/1032855/contributions/4337590/attachments/2234073/3786146/ratemon_update_for_oms_meeting_kmohrman.pdf) (see especially the backup slides)


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

Set up a ssh tunnel through LXPLUS:
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

**Note:** In newer versions <kbd>CTRL</kbd>+<kbd>b</kbd> is used.

On tab 0 you should see the RateMon API server running. If you try `tmux attach -t 0` and get `no sessions`, then you can start a new one by running just `tmux`. If you want to kill the session, run `tmux kill-session -t 0` from the normal shell.

### NGINX

To check what is happening with `nginx`, you can run `systemctl status nginx`. If it is green and shows "running" then it is functioning properly. To start, stop or restart:
- `systemctl start nginx`
- `systemctl stop nginx`
- `systemctl restart nginx`

## Setting up a new CERN OpenStack VM

### Launching a new instance using the CERN OpenStack UI

If you would like to launch a new instance, firstly, go to https://openstack.cern.ch and check whether there is sufficient quota available. If not, you can `Request a Quota Change` (in `Compute` you can untick `Respect the suggested ratios between instances/cores/RAM` to allow for your particular setup in terms of cores & RAM).

To launch a new instance, go to `Compute` -> `Instances` and click `Launch Instance`. Choose an instance name, `C8 - x86_64` for the image, `m2.large` for the flavour and `cms-tsg` as the key pair (which has been uploaded to OpenStack). 

**Note:** You can also `Create Snapshot` of an existing instance and then use that as the image for the new instance (eg. `ater - C8 - x86_64 [2021-06-29]`). In this way, some of the below setup steps (eg. dependencies) can be skipped.

### Setting up the new instance

* Initial setup:
    - After `ssh`ing into the VM, install the necessary dependencies:
    `yum install git root python3 python3-root nginx tmux`
    - Clone the `ratemon` repository:
    `git clone https://gitlab.cern.ch/cms-tsg-fog/ratemon.git`

* Set up the `nginx` config file:
    - Copy the file from an VM that's already set up, located at `/etc/nginx/conf.d/ratemon-api.conf`
    - Remember to change the `server_name` to match the name of your server

* Make a `/cache` directory that's owned by `nginx`:
    ```
    mkdir /cache   
    chown nginx:nginx /cache
    ``` 

* Get the `oracle` rpm:
    ```
    yum install libnsl
    yum install wget
    export LD_LIBRARY_PATH=/usr/lib/oracle/19.6/client64/lib:LD_LIBRARY_PATH
    wget https://download.oracle.com/otn_software/linux/instantclient/19600/oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
    yum install oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
    ```

* Copy over the `tnsnames.ora` file:
    ```
    scp USERNAME@lxplus.cern.ch:/afs/cern.ch/project/oracle/admin/tnsnames.ora .
    mv tnsnames.ora /usr/lib/oracle/19.6/client64/lib/network/admin/
    ```    

* Check if port 80 is open, and if not, open it:
    - First run `firewall-cmd --list-ports`, if you see `80/tcp`, it's already open
    - If not, run `firewall-cmd --add-port=80/tcp` to open it
    - Useful [documentation about firewalls](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/security_guide/sec-controlling_traffic#sec-Controlling_Ports_using_CLI)

* Once things are running, you will need to initialize the `nginx`:
    ```
    systemctl start nginx
    ```

## When things go wrong

- If you try to view the API from your browser (at `http://ater.cern.ch/api/v1/ui/`) and see `"This site can't be reached The webpage at http://ater.cern.ch/api/v1/ui/ might be temporarily down or may ha
ve moved permanently to a new address"`, then probably it needs to be restarted. To restart, start `nginx`, and then run `server.py` inside of a `tmux` session, e.g.:
  ```
  systemctl restart nginx
  cd ratemon/ratemon
  tmux
  python3 server.py
  ```

- This is a good suggestion for most problems as it is a reset for the sever. Try it as a first step, but if it does not solve it, below are a few more troubleshooting situation, mainly regarding an improper VM setup.

- If you try to view the API from your browser and see a 502 ("Bad Gateway") error, then probably main web server (`nginx`) is active but it cannot find the configured applicaiton to show you (in this ca
se the ratemon API). To resolve this issue, first verify that `nginx` is running properly (with `systemctl status nginx`), then attach to the `tmux` session (or start a new one if necessary), and simply 
restart `server.py`. If the problem still persists do:
   ```
   getsebool -a | grep httpd
   ```

- And look to see if ("httpd_can_network_connect") is off. If it is off do:
   ```
   setsebool httpd_can_network_connect 1
   ```

- To set it to on. This should fix the 502 ("Bad Gateway") error. 
