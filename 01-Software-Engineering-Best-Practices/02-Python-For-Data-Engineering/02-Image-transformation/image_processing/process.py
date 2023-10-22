from PIL import Image
import numpy as np
import pathlib
import random
import tensorflow as tf

DATA_PATH = pathlib.Path(__file__).resolve().parent.parent / "data" / "chest_xray"
random.seed(42)


def get_image_paths() -> list:
    """
    Returns a list of all image paths in the data directory inside tuples of the form (label, path) with
    1 for PNEUMONIA and 0 for NORMAL. Make sure that the list is shuffled
    """
    result = []
    #raw_paths = DATA_PATH.glob('**/*.jpeg')
    #for path in raw_paths:
    #    if "/PNEUMONIA/" in str(path): result.append((1, path))
    #    elif "/NORMAL/" in str(path): result.append((0, path))
    for path in DATA_PATH.glob('**/PNEUMONIA/*.jpeg'):
        result.append((1, path))
    for path in DATA_PATH.glob('**/NORMAL/*.jpeg'):
        result.append((0, path))
    random.shuffle(result)
    return result


def process_image(path: str) -> np.ndarray:
    """
    Returns a numpy array of shape (256, 256, 1) with the image data from the given path
    """
    arr = np.array(Image.open(path))
    img = np.resize(arr, (256,256))
    result = np.reshape(img, (256,256,1))
    return result


def write_image(writer, image, label):
    """
    Writes the given image and label to the given writer
    """
    feature = {
        "image": tf.train.Feature(
            bytes_list=tf.train.BytesList(value=[image.tobytes()])
        ),
        "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
    }
    exp = tf.train.Example(features=tf.train.Features(feature=feature)).SerializeToString()
    writer.write(exp)


def main():
    writer = tf.io.TFRecordWriter("dataset.tfrecords")
    for label, path in get_image_paths():
        image = process_image(path)
        write_image(writer, image, label)


if __name__ == "__main__":
    test_img = process_image('/home/janine.windhoff/code/janinewin/data-engineering-challenges/01-Software-Engineering-Best-Practices/02-Python-For-Data-Engineering/02-Image-transformation/data/chest_xray/chest_xray/train/PNEUMONIA/person1465_virus_2530.jpeg')
    print(write_image(tf.io.TFRecordWriter("dataset.tfrecords"), test_img, 1))
