from skimage import data

from lwface import face


def test_face_detection():
    img = data.astronaut()
    patches = face.detect_face(img)
    assert len(patches) > 0

