# Introduction to the RateMon tools

This document is designed to be a reference guide for learning how to run the CMS trigger rate monitoring tools (usually referred to as the “RateMon” tools) for new maintainers/developers of the RateMon tools. The code is in a GitLab repository:

- RateMon GitLab repository: https://gitlab.cern.ch/cms-tsg-fog/ratemon

You should be included as a maintainer of this repository, so if you are not currently listed as a maintainer, please ask someone from the RateMon team to add you.

- Current RateMon team: John Lawrence, Kelci Mohrman, Mateusz Zarucki 

## Background 

For background information about the RateMon tools, feel free to take a look through the materials listed below:

- [Poster that summarizes the main components of the RateMon tools](https://indico.cern.ch/event/587955/contributions/2935746/attachments/1683119/2705019/CHEP_poster_v2.pdf) (Presented by Andrew Wightman at the 2018 CHEP conference) 
- [Slides that summarize the RateMon tools](https://indico.cern.ch/event/805157/contributions/3350524/attachments/1815131/2966314/TSGworkshop_RateMon_talk.pdf
) (Presented by Kelci Mohrman at a 2019 TSG workshop)
- [Slides summarizing the RateMon tools more generally, with a brief overview of the CMS trigger system](https://indico.cern.ch/event/782953/contributions/3464896/attachments/1888644/3114119/RateMon_DPFSlides.pdf) (Presented by Kelci Mohrman at the 2019 APS DPF conference)
- [Slides that provide an update on the current state of the tools](https://indico.cern.ch/event/947284/contributions/3995729/attachments/2093836/3518824/Ratemon_Aug31.pdf) (Presented by Antonio Vivace at a L1T meeting in 2020)
- [CMS paper on the trigger system](https://arxiv.org/pdf/1609.02366.pdf)
- [Antonio Vivace master thesis on the upgrades to RateMon](https://github.com/avivace/master-thesis/releases/download/final-delivery/thesis.pdf)

## Contents

- [How to run RateMon tools - Introduction](intro.md)
- [Notes on using CERN OpenStack VMs](openstack.md)
- [Examples](examples/):
	- [Calling the RateMon API](examples/call_api.py)
