import requests
import argparse
import json
import ROOT

# Example of using this script: python call_api.py 305112

URL_BASE = 'http://ater.cern.ch/api/v1/'

# Set up proxy stuff
#   - I followed the instructions here: https://requests.readthedocs.io/en/master/user/advanced/#socks
#   - Fill in appropriate "host" and "port" info before running the code
PROXIES = {
    'http': 'socks5://user:pass@host:port'
}


# Construct the string to pass to the get function
def construct_request_str(trg,run,datatype):
    if (datatype == "json"):
        s = "ratesJSON?runNumber={run_number}&triggerKey={trg_name}".format(run_number=run,trg_name=trg)
    elif (datatype == "root"):
        s = "ratesROOT?runNumber={run_number}&triggerKey={trg_name}".format(run_number=run,trg_name=trg)
    else:
        print("Unknown datatype:",datatype)
        raise Exception
    return s


# Get a root file and save it to the current directory
def get_root_file(trg,run):

    url = URL_BASE + construct_request_str(trg,run,"root")
    print("\tMaking request...\n\t{url}".format(url=url))
    s = requests.Session()

    # Try to catch "requests.exceptions.InvalidURL: Failed to parse: socks5://user:pass@host:port" error, probably should do this in a better way
    try:
        s.get(url,proxies=PROXIES)
    except requests.exceptions.InvalidURL:
        print("\nERROR: Something may be wrong with the proxy, please check that you have entered proper host and port info.\n")
        raise Exception

    # Get the data
    r = s.get(url,proxies=PROXIES)
    status = r.status_code
    data = r.content
    print("\tStatus of request:",status)

    # Save to a root file
    with open(trg+".root", "wb") as savef:
        savef.write(data)


# Save the png of the root file
def save_png(trg,rootfname):
    tf = ROOT.TFile.Open(rootfname)
    h = tf.Get(trg+"_< PU >_vs_pre-deadtime unprescaled rate")
    h.Draw("h")
    h.Print(trg+".png")


def main():

    # The run is passed as an argument, should we be able to pass more than one run?
    parser = argparse.ArgumentParser()
    parser.add_argument("run",type=int)
    args = parser.parse_args()
    run = args.run

    # Trigger list is hard coded for now...
    #   - Could have it as an arguemnt that we pass to the script
    #   - Or read the list from a file
    trg_lst = ["HLT_CaloJet500_NoJetID"]

    # Loop over triggers in list, get the root file for each, and save it and the png
    for trg in trg_lst:
        print("\nMaking plot for trigger:",trg)
        get_root_file(trg,run)
        save_png(trg,trg+".root")


main()
