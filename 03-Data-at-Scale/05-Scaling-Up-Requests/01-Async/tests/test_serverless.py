import os
import pathlib

def test_dockerfile():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dockerfile_fp = os.path.join(parent_dir, "Dockerfile")
    contents = open(dockerfile_fp).read()
    assert len(contents) > 10, "The Dockerfile seems a little empty"


def test_registry_prefix():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    makefile_fp = os.path.join(parent_dir, "Makefile")
    line = [l.strip() for l in open(makefile_fp) if l.startswith("REGISTRYPREFIX=")][0]
    # Assume the REGISTRYPREFIX= is at least 5 characters long (in practice it's probably more)
    assert len(line) > len("REGISTRYPREFIX=") + 5, "Seems like you haven't filed the REGISTRYPREFIX value in the Makefile"
