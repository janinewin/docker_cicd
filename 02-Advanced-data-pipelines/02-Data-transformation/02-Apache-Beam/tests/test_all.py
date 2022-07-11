import os
import pathlib

from lwmr import impl_python, impl_mapreduce, impl_pyspark, impl_beam

TXT = "I love apples, bananas and apples"


def test_txt_file_exists():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    txt_fp = os.path.join(parent_dir, "data", "The_Data_Engineering_Cookbook.txt")
    assert os.path.isfile(
        txt_fp
    ), "Please download the file https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/data-engineering-cookbook-book/The_Data_Engineering_Cookbook.txt under ./data/"


def test_python_impl():
    cnt = impl_python.count_words(TXT)
    assert cnt.get("apples") == 2, "'Apples' is expected to be found 2 times"
    assert cnt.get("I") == 1, "'I' is expected to be found 1 time"


def test_mapreduce_impl():
    cnt = impl_mapreduce.count_words(TXT)
    assert cnt.get("apples") == 2, "'Apples' is expected to be found 2 times"
    assert cnt.get("I") == 1, "'I' is expected to be found 1 time"


def test_pyspark_impl():
    cnt = impl_pyspark.count_words(TXT)
    assert cnt.get("apples") == 2, "'Apples' is expected to be found 2 times"
    assert cnt.get("I") == 1, "'I' is expected to be found 1 time"


def test_beam_impl():
    cnt = impl_beam.count_words(TXT)
    assert cnt.get("apples") == 2, "'Apples' is expected to be found 2 times"
    assert cnt.get("I") == 1, "'I' is expected to be found 1 time"
