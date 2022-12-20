import glob
import os
import pathlib
from typing import Dict

from lwmr import text_processing

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from apache_beam.io import ReadFromText, WriteToText


class WordExtractingDoFn(beam.DoFn):
    def process(self, row: str):
        """
        Given a line, we return the words using our `text_processing.get_words` function used in other implementations
        """
        pass  # YOUR CODE HERE


def read_results(output_dir: str, prefix_fn: str):
    """
    The results from the BEAM runner are spread across multiple files.
    We provide a helper function to read the results back to a single Python dictionary. 
    """
    fps = glob.glob(f"{os.path.join(output_dir, prefix_fn)}*")
    counts = {}
    for fp in fps:
        with open(fp) as f:
            for l in f:
                word, count_str = l.strip().split(":=")
                if word in counts:
                    counts[word] += int(count_str)
                else:
                    counts[word] = int(count_str)
    return counts


def format_result(word: str, count: int):
    """
    Format the counts into a PCollection of strings.
    """
    return '%s:=%d' % (word, count)


def count_words(file_path: str) -> Dict[str, int]:
    """
    Counting words as a Beam pipeline
    """
    # Set up the pipeline with default options
    pipeline_options = PipelineOptions()
    pipeline_options.view_as(SetupOptions).save_main_session = True

    output_dir = "/tmp/beam-output/"
    prefix_fn = "test-output.txt"
    output_fps_prefix = os.path.join(output_dir, prefix_fn)
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    with beam.Pipeline(options=pipeline_options) as p:
        # Read the text file[pattern] into a PCollection.
        lines = None
        pass  # YOUR CODE HERE

        words = (
            lines
            | 'Split' >> (beam.ParDo(WordExtractingDoFn()).with_output_types(str))
        )

        counts = (
            words
            | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
            | 'GroupAndSum' >> beam.CombinePerKey(sum))

        output = counts | 'Format' >> beam.MapTuple(format_result)

        # We write the output to files with the prefix `output_fps_prefix`
        output | 'Write' >> WriteToText(output_fps_prefix)

    # Read the counts back from the files and return it
    counts = read_results(output_dir, prefix_fn)

    return counts
