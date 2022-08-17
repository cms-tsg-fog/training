# Advanced options for plotTriggerRates.py

This goes into further details about less common options for plotTriggerRates.py.

This requires the setup in the `intro.md` document. Follow those instructions and ensure that `plotTriggerRates.py` runs as expected.

## Update the online reference fits

The first step is to select the reference runs. They should: have a wide range of pileup, be long runs, have no issues listed in the run registry, and produce good fits for the monitored triggers at least. A good example of this, is the previous runs for the reference fits. More exact numbers of these can be obtained by examining those
To make the fits run the following commands:

```
python3 plotTriggerRates.py --allTriggers --updateOnlineFits runNumbers

python3	plotTriggerRates.py --triggerList=TriggerLists/monitorlist_COLLISIONS.list --updateOnlineFits runNumbers
```

This will create the reference fits for all triggers and the monitored triggers respectively. Once the fits are created, the plots created should be examined to ensure everything is correct.
Once the fits are created, they can be committed to the respoitory. A new tag will need to be created and deployed to P5.

## Running in certification (secondary) mode 

This creates some plots and .txt files to help with run certification typically done by the secondary HLT DOC

To run in secondary mode and certify runs based on rates the monitor triggers in the collisions list and make plots of rate vs LS:

```
python3 plotTriggerRates.py --Secondary --triggerList=monitorlist_COLLISIONS.list --fitFile=Fits/Monitored_Triggers/FOG.pkl yourRunNumbers
```

Note: The fit file FOG.pkl is updated regularly and contains the latest fits. If there are questions about the fit, ask in the RateMon channel in mattermost

The summary of all the results is dumped into a text file labeled badLumiSummary_runXXX_runYYY.txt which lists for every run:

All of the bad triggers and the corresponding bad ls
A list of the LS sorted by the "worst" LS (worst = most triggers deviating from fit) 

The results are dumped into a directory titled CertificationSummary _xxxx-yyyy, where xxxx and yyy are the minimum and maximum run numbers you specified on the command line. Inside this directory there is:

- A .txt file listing the bad LS and bad triggers
- A directory titled 'png' containing png files of every plot in the .root file 

Notes:

- Fits are automatically adjusted for deadtime, prescale
- All rates plotted by default are raw unprescaled rates
- The acceptable tolerance (default = 3sigma) from fit is what determines a bad LS. When the rate for the run being certified is beyond the 3sigma error band, the LS is marked bad. 

## Other Options

This lists other options in `plotTriggerRates.py` and some examples

- --createFit
   - This option tells the code to generate a best fit function for the specified data. The fit file will be saved in the same directory as the .root file and will be saved as fit_file.pkl
   - Ex: `python3 plotTriggerRates.py --createFit 123 132 213 231`
- --bestFit
   - By default the code will only attempt to create a quadratic fit to the data, but if you use this option it will also generate a linear and sinh fit and then pick the one with the smallest mean square error as the 'best' fit.
   - Ex: `python3 plotTriggerRates.py --createFit --bestFit 123 132 213 231`
- --multiFit
   - This option tells the plot maker for each trigger to display as many fits as it knows about, all on the same plot.
   - Ex: `python3 plotTriggerRates.py --createFit --multiFit 123 132 213 231`
- --useFit=<fit_type>
   - This option allows you to override the 'default' fit to use and instead try a different fit function. The current list of supported fits are: 'linear', 'quad', 'cube', 'exp', and 'sinh'
   - Ex: `python3 plotTriggerRates.py --createFit --useFit=linear 123 132 213 231`
- --fitFile=<fit_file>
   - This option allows you specify a .pkl file which contains previously generated fits, that the code will display on top of the rate data
   - Ex: `python3 plotTriggerRates.py --fitFile=/path/to/fit_file.pkl 123 132 213 231`
- --triggerList=<your_trigger_list>
   - Specify a particular list of triggers that you want plotted
   - Ex: `python3 plotTriggerRates.py --triggerList=/path/to/trigger_file.list 123 132 213 231`
- --vsInstLumi / --vsLS
   - Generate Rate vs. Inst. Luminosity (LS) plots
   - Ex1: `python3 plotTriggerRates.py --vsInstLumi 123 132 213 231`
   - Ex2: `python3 plotTriggerRates.py --vsLS 123 132 213 231`
- --useCrossSection
   - Scales the y-values, by dividing each plot point by its corresponding inst. luminosity
   - Ex: `python3 plotTriggerRates.py --useCrossSection 123 132 213 231`
   - Note: This option does not normalize by the number of colliding bunches 
- --psFilter=1,2,3
   - This option will only plot points that were produced in the specified prescale columns
   - Ex: `python3 plotTriggerRates.py --psFilter=1,2,4 123 132 213 231`
- --useFills
   - This option allows you to specify entire fills to plot instead of individual runs
   - Ex: `python3 plotTriggerRates.py --useFills 1234 4321
- --saveDirectory=/path/to/some/dir
   - This option allows you to save the plots to a specific output directory
   - Ex: `python3 plotTriggerRates.py --saveDirectory=/path/to/some/directory 123 132 213 231`
   - Note: If the output directory already exists the code will attempt to remove all contents from that directory first! 

By default the output of the script will produce the plots in a directory labeled tmp_rate_plots. In this directory you will find:

- A .pkl file for use in secondary mode and for the online rate monitoring tool
- An index.html files so you can easily copy this directory to your web area and quickly view your plots online.
- A png/ directory containing all the plots as individual .png files 

There are many other features of this program. For more information, or just for fun, try typing:

```
python3 plotTriggerRates.py --Help 
```