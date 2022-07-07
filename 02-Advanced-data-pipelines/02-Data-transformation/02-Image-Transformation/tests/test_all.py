import pathlib
import os

from skimage import data

from lwface import face


def test_face_detection():
    img = data.astronaut()
    patches = face.detect_face(img)
    assert len(patches) > 0


def test_dockerfile():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dockerfile_fp = os.path.join(parent_dir, "Dockerfile")
    found = False
    for l in open(dockerfile_fp):
        if "Delete this line when you've read the full Dockerfile" in l:
            found = True
    assert not found, "Have you read the Dockerfile until the end? There is an instruction at the very end."


def test_registry_prefix():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    makefile_fp = os.path.join(parent_dir, "Makefile")
    line = [l.strip() for l in open(makefile_fp) if l.startswith("REGISTRYPREFIX=")]
    # Assume the REGISTRYPREFIX= is at least 5 characters long (in practice it's probably more)
    assert len(line) > len("REGISTRYPREFIX=") + 5, "Seems like you haven't filed the REGISTRYPREFIX value in the Makefile"
