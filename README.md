Plankton are effective indicators of environmental change and ecosystem health in freshwater habitats, but collection of plankton data using manual microscopic methods is extremely labor-intensive and expensive. Automated plankton imaging offers a promising way forward to monitor plankton communities with high frequency and accuracy in real-time. Yet, manual annotation of millions of images proposes a serious challenge to taxonomists. Deep learning classifiers have been successfully applied here to categorize marine plankton images. The Kiso experiment runs a plankton classification workflow.

# Getting Started

## Prerequisites

```sh
pip install kiso
pip install kiso[chameleon]
```

## Running the experiment

Create application credentials for CHI@Edge as `edge-app-cred-oac-edge-openrc.sh` and CHI@TACC as `tacc-app-cred-oac-edge-openrc.sh`
and place the files in the `secrets` directory.

## Running the experiment

```sh
# Check Kiso experiment configuration
kiso check

# Provision and setup the resources
kiso up

# Run the experiments defined in the experiment configuration YAML file
kiso run

# Destroy the provisioned resources
kiso down

# Pegasus workflow submit directories will be placed in the output directory at the end of the experiment. The submit directories will also have a statistics directory with the pegasus-statistics output.
# Outputs defined in the experiment configuration will be placed in the destination specified in the experiment configuration.
```

# References

- [Pegasus Workflow Management System](https://pegasus.isi.edu)
- [EnOSlib](https://discovery.gitlabpages.inria.fr/enoslib/)
- [Chameleon Cloud](https://www.chameleoncloud.org)
- [FABRIC](https://portal.fabric-testbed.net)

# Citation

- [Kyathanahally, S. P., Hardeman, T., Merz, E., Bulas, T., Reyes, M., Isles, P., Pomati, F., & Baity-Jesi, M. (2021). Deep Learning Classification of Lake Zooplankton. Frontiers in Microbiology, 12.](https://doi.org/10.3389/fmicb.2021.746297)

# Acknowledgements

Kiso is funded by National Science Foundation (NSF) under award [2403051](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2403051).
