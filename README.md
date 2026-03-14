# Kiso Plankifier Experiment

> A plankton classification workflow that automates image annotation using deep learning,
> running on distributed infrastructure via Pegasus and Chameleon Cloud.

Plankton are effective indicators of ecosystem health, but manual microscopic annotation
of images is labor-intensive at scale. This experiment runs an end-to-end deep learning
classification workflow over automated plankton images using the [Kiso](https://github.com/pegasus-isi/kiso)
framework.

## Prerequisites

- Python 3.9+
- Access to [CHI@Edge](https://chameleoncloud.org) and [CHI@TACC](https://chameleoncloud.org) (Chameleon Cloud accounts)

```sh
pip install kiso
pip install kiso[chameleon]  # required for Chameleon Cloud provisioning
```

## Configuration

Create application credentials for CHI@Edge and CHI@TACC and place them in the `secrets/` directory:

```
secrets/
  edge-app-cred-oac-edge-openrc.sh   # CHI@Edge credentials
  tacc-app-cred-oac-edge-openrc.sh   # CHI@TACC credentials
```

See [Chameleon Cloud docs](https://chameleoncloud.org/docs) for how to generate application credentials.

## Running the Experiment

```sh
# Validate the experiment configuration
kiso check

# Provision and set up resources
kiso up

# Run the experiment
kiso run

# Check the output
cat count.txt

# Tear down provisioned resources
kiso down
```

## Outputs

Pegasus workflow submit directories are written to the `output/` directory when the experiment completes.
Each submit directory includes a `statistics/` subdirectory with `pegasus-statistics` output.
Additional outputs are placed at the destinations specified in `experiment.yml`.

## References

- [Pegasus Workflow Management System](https://pegasus.isi.edu) — scientific workflow engine used to define and execute experiments in Kiso
- [EnOSlib](https://discovery.gitlabpages.inria.fr/enoslib/) — infrastructure management library that Kiso builds on for provisioning and remote execution
- [Chameleon Cloud](https://www.chameleoncloud.org) — NSF-funded cloud testbed supported by Kiso
- [FABRIC](https://portal.fabric-testbed.net) — nationwide programmable research infrastructure supported by Kiso

## Citation

Kyathanahally et al. (2021). [Deep Learning Classification of Lake Zooplankton](https://doi.org/10.3389/fmicb.2021.746297). *Frontiers in Microbiology, 12*.

## Acknowledgements

Kiso is funded by the National Science Foundation (NSF) under award [2403051](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2403051).

## License

Apache 2.0 © [Pegasus ISI](https://github.com/pegasus-isi)
