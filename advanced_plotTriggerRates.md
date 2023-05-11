# Advanced options for plotTriggerRates.py

This goes into further details about less common options for `plotTriggerRates.py`.

This requires the setup in the `intro.md` document. Follow those instructions and ensure that `plotTriggerRates.py` runs as expected.

## Update the online reference fits

When the reference fits need to be updated (because they were requested, there are too many fake alerts, or another reason), the first step is to select the runs used to make the new plots. The runs must meet the following criteria:

Reference Fit criteria
- Must be more recent than previous reference runs
- At least 2 runs, each longer than 100 LS (preferably total LS between all runs >400)
- Marked as good in RR
- When run over the same runs in secondary using fits made from the runs <5% lumisection marked as bad
- All fits from the monitored_trigger list should be visually inspected to ensure no significant deviation is seen
- Must cover a large range of PU. 20-50 PU is preferrable

After the runs have been selected, the fits can be made. To make the fits run the following commands:

```
python3 plotTriggerRates.py --allTriggers --updateOnlineFits runNumbers

python3	plotTriggerRates.py --triggerList=TriggerLists/monitorlist_COLLISIONS.list --updateOnlineFits runNumbers
```

This will create the reference fits for all triggers and the monitored triggers respectively. Hence you can see updated files of `FOG.pkl` and `command_line.txt` both in `Fits/All_Triggers` and `Fits/Monitor_Triggers` directories. 

Once the fits are created, the plots are also created in the `plots` directory inside these same two trigger directories. The plots should be examined to ensure everything is correct.

Once the fits are created (and plots look fine), commit the four files to the respoitory: `Fits/All_Triggers/FOG.pkl`, `Fits/All_Triggers/command_line.txt`, `Fits/Monitor_Triggers/FOG.pkl` and Fits/Monitor_Triggers/command_line.txt`. 
 
Then create a new tag from the new commit and a new pipeline to deploy it to P5. See section Deployment under [ratemon instruction](https://gitlab.cern.ch/cms-tsg-fog/ratemon/-/blob/master/README.md) for details.

To see how the current fits were created, the `command_line.txt` file in `Fits` folder in the RateMon repository as mentioned above shows the command used to create the fits.

## Running in certification (secondary) mode 

This creates some plots and .txt files to help with run certification typically done by the secondary HLT DOC

To run in secondary mode and certify runs based on rates the monitor triggers in the collisions list and make plots of rate vs LS:

```
python3 plotTriggerRates.py --Secondary --triggerList=TriggerLists/monitorlist_COLLISIONS.list --fitFile=Fits/Monitor_Triggers/FOG.pkl yourRunNumbers
```

Note: The fit file FOG.pkl is updated regularly and contains the latest fits. If there are questions about the fit, ask in the RateMon channel in mattermost

The summary of all the results is dumped into a text file labeled badLumiSummary_runXXX_runYYY.txt which lists for every run:

All of the bad triggers and the corresponding bad ls
A list of the LS sorted by the "worst" LS (worst = most triggers deviating from fit) 

The results are dumped into a directory titled CertificationSummary _xxxx-yyyy, where xxxx and yyy are the minimum and maximum run numbers you specified on the command line. Inside this directory there is:

- A .txt file listing the bad LS and bad triggers
- A directory titled 'png' containing png files of every plot 

Notes:

- Fits are automatically adjusted for deadtime, prescale
- All rates plotted by default are raw unprescaled rates
- The acceptable tolerance (default = 5sigma) from fit is what determines a bad LS. When the rate for the run being certified is beyond the 3sigma error band, the LS is marked bad. 

Interperting the results:

- These results require interpertation, as some LS are marked as bad even when they are not
- Isolated LS that are only marked as bad and not the surrounding LS for 2 to 3 triggers can be ignored as small spikes are common
- Groups of LS marked as bad should be investigated
- Any LS with very large deviations (can be seen on hte rate vs. LS plots produced here) should be investigated

This option will run the certification for the monitored triggers. If you want to run the script over all triggers in the runs you can do:

```
python3 plotTriggerRates.py --Secondary --allTriggers --fitFile=Fits/All_Triggers/FOG.pkl yourRunNumbers
```

## Total L1 Plots

To create the plots for total L1 rates use the following command:

```
python3 plotTriggerRates.py --L1ARate yourRunNumbers
```

This will create the following rate vs. PU plots
- Total L1A Rate
- Total L1A Rate Pre-dt
- L1A Physics
- L1A Physics Lost

## Dataset Plots

To create rate vs. PU plots for all of the datatsets in a run use the following command:

```
python3 plotTriggerRates.py --datasetRate yourRunNumbers
```

## Other Options

This lists other options in `plotTriggerRates.py` and some examples

- --createFit
   - This option tells the code to generate a best fit function for the specified data. The fit file will be saved in the same directory as the .root file and will be saved as fit_file.pkl
   - Ex: `python3 plotTriggerRates.py --createFit yourRunNumbers`
- --bestFit
   - By default the code will only attempt to create a quadratic fit to the data, but if you use this option it will also generate a linear and sinh fit and then pick the one with the smallest mean square error as the 'best' fit.
   - Ex: `python3 plotTriggerRates.py --createFit --bestFit yourRunNumbers`
- --multiFit
   - This option tells the plot maker for each trigger to display as many fits as it knows about, all on the same plot.
   - Ex: `python3 plotTriggerRates.py --createFit --multiFit yourRunNumbers`
- --useFit=<fit_type>
   - This option allows you to override the 'default' fit to use and instead try a different fit function. The current list of supported fits are: 'linear', 'quad', 'cube', 'exp', and 'sinh'
   - Ex: `python3 plotTriggerRates.py --createFit --useFit=linear yourRunNumbers`
- --fitFile=<fit_file>
   - This option allows you specify a .pkl file which contains previously generated fits, that the code will display on top of the rate data
   - Ex: `python3 plotTriggerRates.py --fitFile=/path/to/fit_file.pkl yourRunNumbers`
- --triggerList=<your_trigger_list>
   - Specify a particular list of triggers that you want plotted
   - Ex: `python3 plotTriggerRates.py --triggerList=/path/to/trigger_file.list yourRunNumbers`
- --vsLS
   - Generate Rate vs. LS plots
   - Ex: `python3 plotTriggerRates.py --vsLS yourRunNumbers`
- --psFilter=1,2,3
   - This option will only plot points that were produced in the specified prescale columns
   - Ex: `python3 plotTriggerRates.py --psFilter=1,2,4 yourRunNumbers`
- --useFills
   - This option allows you to specify entire fills to plot instead of individual runs
   - Ex: `python3 plotTriggerRates.py --useFills yourFillNumbers
- --saveDirectory=/path/to/some/dir
   - This option allows you to save the plots to a specific output directory
   - Ex: `python3 plotTriggerRates.py --saveDirectory=/path/to/some/directory yourRunNumbers`
   - Note: If the output directory already exists the code will attempt to remove all contents from that directory first! 

By default the output of the script will produce the plots in a directory labeled tmp_rate_plots. In this directory you will find:

- A .pkl file for use in secondary mode and for the online rate monitoring tool
- An index.html files so you can easily copy this directory to your web area and quickly view your plots online.
- A png/ directory containing all the plots as individual .png files 

There are many other features of this program. For more information, or just for fun, try typing:

```
python3 plotTriggerRates.py --Help 
```
