import os
import pathlib

from lwserverless.app import fast_run_wait_time_seconds, slow_run_wait_time_seconds


def test_times():
    def is_number(v):
        return isinstance(v, int) or isinstance(v, float)

    assert is_number(fast_run_wait_time_seconds()), "Please give a float value to `fast_run_wait_time_seconds`"
    assert is_number(slow_run_wait_time_seconds()), "Please give a float value to `slow_run_wait_time_seconds`"


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


def test_runtimes_concurrency():
    from lwserverless import runs
    assert runs.runtime_15() < runs.runtime_25(), "Did you run the statistics and fill in the `lwserverless/runs.py` file"
