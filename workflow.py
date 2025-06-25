#!/usr/bin/env python3
import logging
import os
from argparse import ArgumentParser
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

# --- Import Pegasus API ------------------------------------------------------
from Pegasus.api import *


class PlankifierWorkflow:
    wf = None
    sc = None
    tc = None
    props = None

    dagfile = None
    wf_name = None
    wf_dir = None

    # --- Init ----------------------------------------------------------------
    def __init__(self, dagfile="workflow.yml"):
        self.dagfile = dagfile
        self.wf_name = "plankifier-wf"
        self.wf_dir = str(Path(__file__).parent.resolve())

    # --- Write files in directory --------------------------------------------
    def write(self):
        if not self.sc is None:
            self.sc.write()
        self.props.write()
        self.tc.write()
        self.wf.write()

    # --- Configuration (Pegasus Properties) ----------------------------------
    def create_pegasus_properties(self):
        self.props = Properties()

        # props["pegasus.monitord.encoding"] = "json"
        # self.properties["pegasus.integrity.checking"] = "none"
        return

    # --- Site Catalog --------------------------------------------------------
    def create_sites_catalog(self, exec_site_name="condorpool"):
        self.sc = SiteCatalog()

        shared_scratch_dir = os.path.join(self.wf_dir, "scratch")
        local_storage_dir = os.path.join(self.wf_dir, "output")

        local = Site("local").add_directories(
            Directory(Directory.SHARED_SCRATCH, shared_scratch_dir).add_file_servers(
                FileServer("file://" + shared_scratch_dir, Operation.ALL)
            ),
            Directory(Directory.LOCAL_STORAGE, local_storage_dir).add_file_servers(
                FileServer("file://" + local_storage_dir, Operation.ALL)
            ),
        )

        exec_site = (
            Site(exec_site_name)
            .add_pegasus_profile(style="condor")
            .add_condor_profile(universe="vanilla")
            .add_profiles(Namespace.PEGASUS, key="data.configuration", value="condorio")
        )

        self.sc.add_sites(local, exec_site)

    # --- Transformation Catalog (Executables and Containers) -----------------
    def create_transformation_catalog(self, exec_site_name="condorpool"):
        self.tc = TransformationCatalog()
        w = Transformation(
            "worker",
            namespace="pegasus",
            site="condorpool",
            pfn="https://download.pegasus.isi.edu/pegasus/5.1.1/pegasus-worker-5.1.1-x86_64_rhel_8.tar.gz",
            is_stageable=True,
        )

        plankifier = Transformation(
            "plankifier",
            site=exec_site_name,
            pfn="/srv/plankifier/predict.py",
            is_stageable=False,
        )
        count = Transformation(
            "count",
            site=exec_site_name,
            pfn=(Path(".") / "bin/count.sh").resolve(),
            is_stageable=True,
        )

        self.tc.add_transformations(plankifier, count, w)

    # --- Create Workflow -----------------------------------------------------
    def create_workflow(self):
        self.wf = Workflow(self.wf_name, infer_dependencies=True)

        matches = File("predict_unanimityabs0.6.txt")
        plankifier_job = (
            Job("plankifier")
            .add_args(
                "-modelfullnames", "/srv/plankifier/trained-models/conv2/keras_model.h5"
            )
            .add_args(
                "-weightnames", "/srv/plankifier/trained-models/conv2/bestweights.hdf5"
            )
            .add_args("-testdirs", "/srv/plankifier/camera-images")
            .add_args("-thresholds", "0.6")
            .add_args("-ensMethods", "unanimity")
            .add_args("-predname", "./predict")
            .add_outputs(matches, stage_out=True)
            .add_condor_profile(
                requirements='DC_ID == "dc-1" && TARGET.Arch == "AARCH64"'
            )
        )

        count = File("count.txt")
        count_job = (
            Job("count")
            .add_args(matches, count)
            .add_inputs(matches)
            .set_stdout(count, stage_out=True, register_replica=True)
        )

        self.wf.add_jobs(plankifier_job, count_job)


if __name__ == "__main__":
    parser = ArgumentParser(description="Pegasus Pipeline Workflow")

    parser.add_argument(
        "-s",
        "--skip_sites_catalog",
        action="store_true",
        help="Skip site catalog creation",
    )
    parser.add_argument(
        "-e",
        "--execution_site_name",
        metavar="STR",
        type=str,
        default="condorpool",
        help="Execution site name (default: condorpool)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="STR",
        type=str,
        default="workflow.yml",
        help="Output file (default: workflow.yml)",
    )

    args = parser.parse_args()

    workflow = PlankifierWorkflow(args.output)

    if not args.skip_sites_catalog:
        print("Creating execution sites...")
        workflow.create_sites_catalog(args.execution_site_name)

    print("Creating workflow properties...")
    workflow.create_pegasus_properties()

    print("Creating transformation catalog...")
    workflow.create_transformation_catalog(args.execution_site_name)

    print("Creating pipeline workflow dag...")
    workflow.create_workflow()

    workflow.write()
    workflow.wf.plan(submit=True)
