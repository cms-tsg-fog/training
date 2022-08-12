# Update the online reference fits

These are the current instructions for updating the reference fits for RateMon

This requires running `plotTriggerRates.py`, so follow the setup instructions in the `intro.md` document and ensure that runs as expected.

The first step is to select the reference runs. They should: have a wide range of pileup, be long runs, have no issues listed in the run registry, and produce good fits for the monitored triggers at least. A good example of this, is the previous runs for the reference fits. More exact numbers of these can be obtained by examining those

To make the fits run the following commands:

```
python3 plotTriggerRates.py --allTriggers --updateOnlineFits runNumbers

python3	plotTriggerRates.py --triggerList=TriggerLists/monitorlist_COLLISIONS.list --updateOnlineFits runNumbers
```

This will create the reference fits for all triggers and the monitored triggers respectively. Once the fits are created, the plots created should be examined to ensure everything is correct. 

Once the fits are created, they can be committed to the respoitory. A new tag will need to be created and deployed to P5.

