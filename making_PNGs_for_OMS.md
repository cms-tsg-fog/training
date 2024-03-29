# Making the rate vs PU PNG files to be displayed on OMS

The VM `kvm-s3562-1-ip151-84` is used for this task. The `ratemon` repository is located inside of the `/opt/` directory on the VM. The PNG files that the code creates can be saved in a subdirectory of the `/cmsnfsrateplots/rateplots/` directory (`Run2`, `Run3`, `LS2`, or `testing`).

**Important**: Always become `hltpro` before doing anything on this VM!  

The wrapper script responsible for producing the rate vs PU plots is `make_plots_for_cron.py`. Currently, the script uses the `oldParser` option when running `plotTriggerRates` since the code requires the `getPathsInDatasets()` function, which is not available with the new parser ([Issue #31](https://gitlab.cern.ch/cms-tsg-fog/ratemon/-/issues/31)).

## For reference: operations during Run 2 data taking
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

## Dependencies 

The `kvm-s3562-1-ip151-84` machine by default does not have many of the dependencies that the RateMon code requires. It can be easy to overlook the dependencies that are available by default on `lxplus` (since we generally test the code on `lxplus`), so for reference we have compiled a list of the dependencies that we had to request to be installed on `kvm-s3562-1-ip151-84` (for python3):
```
python 3.6
cx_Oracle
yaml
setuptools
requests
ROOT
```
If the code requires packages that are not available on `kvm-s3562-1-ip151-84`, just open a CMS ONS JIRA ticket to request that the packages be installed (examples: [CMSONS-13369](https://its.cern.ch/jira/browse/CMSONS-13369), [CMSONS-13163](https://its.cern.ch/jira/browse/CMSONS-13163), [CMSONS-13241](https://its.cern.ch/jira/browse/CMSONS-13241)).

## cron

We use `cron` to run the `make_plots_for_cron.py` script periodically. This is specified via the `crontab` file. A reference that explains how to use `cron` is [here](https://www.adminschoice.com/crontab-quick-reference).

 To display the list of cron jobs in the `crontab` file, run `crontab -l`. To edit the file, run `crontab -e`.

Each line in the `crontab` file should specify a command to run, and the frequency at which it should be executed (as described in the reference above). For our `make_plots_for_cron.py` script, the line in the `crontab` file is this:
```
1 * * * * python3 /data/ratemon/ratemon/make_plots_for_cron.py > /dev/null
```
This specifies that the file should be run once per hour on the 1st minute of the hour, and that the output should be directed to `dev/null`. Lines in the `crontab` file that begin with a `#` will not be executed. 

Note that for running `make_plots_for_cron.py` with `cron`, it is important that all file paths are absolute.

If your the `cron` job runs into an error, the error message can be found in `/var/spool/mail/hltpro`.

