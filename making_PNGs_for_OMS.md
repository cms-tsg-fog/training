# Making the rate vs PU PNG files to be displayed on OMS

The VM `kvm-s3562-1-ip151-84` is used for this task. The `ratemon` repository is located inside of the `/data/` directory on the VM. OMS looks for the outpout PNG files in the `/cmsnfsrateplots/rateplots/RUNNUMBER` directory.

**Important**: Always become `hltpro` before doing anything on this VM!  

## Operations during Run 2 data taking
During Run 2 data taking, a cron job ran the [make_plots_for_cron.sh](https://gitlab.cern.ch/cms-tsg-fog/ratemon/-/blob/master/ratemon/make_plots_for_cron.sh) once per hour. The bash script ran `plotTriggerRates.py` to create rate vs PU plots for the latest fill with stable beams, then copied the plots and `index.html` files to `/cmsnfsrateplots/rateplots/`, where WMB would find and display them.

## How to access the machine

First ssh into `lxplus`, then `cmsusr`. Next, ssh into the VM. Always become `hltpro` before doing anything on this VM, so that `hltpro` will be the owner of the repository and all of the files inside of it. To summarize these steps:
```
ssh -Y [your user name]@lxplus.cern.ch
ssh cmsusr
ssh -Y [your user name]@kvm-s3562-1-ip151-84.cms
sudo -u hltpro -i
```

In general, we only pull from this machine, and do not usually push from it. If you are developing relevant scripts, write and test the scripts on `lxplus`, then commit and push to a branch when you are ready. Then, from this VM, use `git pull` to access the updates.  To perform a `git pull` from this machine, you will need to run the following command to start the proxy:
```
ssh -f -N -D 1080 [your user name]@cmsusr.cms
```
This will require your `cmsusr` password. After this command, you should be able to e.g. `git clone` the repository using the `https` method. More information about this command and about how git through a proxy can be found [here](https://cms-sw.github.io/tutorial-proxy.html). 
