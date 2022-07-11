from collections import Counter
from typing import Dict, List, Tuple

import numpy as np

from lwmr import text_processing


def split_words_into_groups(words: List[str], n_buckets: int = 5) -> List[List[str]]:
    """
    Split an input list like ["I", "am", "a", "sentence"] into a given number of buckets
    For instance split_words_into_groups(["I", "am", "a", "sentence"], n_buckets = 3)
    should return [["I", "am"], ["a"], ["sentence"]] 

    Try the np.array_split(...) function.
    """
    pass  # YOUR CODE HERE


def simple_map_word_to_word_and_one(word_group: List[str]) -> List[Tuple[str, int]]:
    """
    This function is a bit odd but necessary to respect conventions of the map / reduce world where the result of a map function
    is of the format (key, value).
    Here the key is the word and the value is always 1.
    """
    return [
        (word, 1)
        for word in word_group
    ]


def map_on_each_group(word_groups: List[List[str]]) -> List[List[Tuple[str, int]]]:
    """
    map_on_each_group simply applies the function simple_map_word_to_word_and_one onto each group
    coming from split_words_into_groups
    """
    pass  # YOUR CODE HERE


def shuffle(word_groups_with_counts: List[List[Tuple[str, int]]]) -> Dict[str, List[int]]:
    """
    shuffle aggregates word counts for each group into a dictionary word -> list of counts
    
    For instance it takes as input
    [
        [("hello", 1), ("world", 1)],
        [("hello", 1)],
    ]

    to return
    {
        "hello": [1, 1],
        "world": [1]
    }
    """
    clusters_map = {}
    for word_group in word_groups_with_counts:
        for word, count in word_group:
            # If this word has never been seen, add it to the clusters map
            if word not in clusters_map:
                clusters_map[word] = []
            # Add the entry count to this word's key in the clusters_map dictionary
            clusters_map[word].append(count)
    # To follow map / reduce conventions, return a list (or a map) where each entry is of the form
    # (key, [value1, value2, value3, ...])
    return clusters_map


def count_within_group(word: str, counts: List[int]) -> Tuple[str, int]:
    """
    Given a word and a "silly" list of ones, return the word and its total count: (word, count)
    """
    total_count = 0

    # Fill the code below, given a list of individual counts from the various word groups
    # to return the total counts
    pass  # YOUR CODE HERE
    return word, total_count


def final_reduce(groups: List[Tuple[str, List[int]]]) -> List[Tuple[str, int]]:
    """
    Apply count_within_group on each group and return a list where each element is the (word, total_count)
    """
    return [count_within_group(word, counts) for word, counts in groups.items()]


def count_words(txt: str) -> Dict[str, int]:
    """
    count_words implements serially all of the map/reduce steps described in the diagram 
    """
    # From the raw text, extract the list of words with nltk
    words = text_processing.get_words(txt)

    # From a single list of words to groups of list of words - we're spreading the load evenly across workers
    word_groups = split_words_into_groups(words, 5)

    # Apply a mapping function on each group, in production this would happen on several servers in a cluster
    mapped_groups = map_on_each_group(word_groups)

    # Shuffle / Group the results of individual groups, by a key, the "word" we're counting
    shuffled_groups = shuffle(mapped_groups)

    # Finally reduce each group to count the number of occurrences of each word, then aggregate into a single list
    final_result = final_reduce(shuffled_groups)

    # Transform the list of (word, count) into a dictionary keyed by the word, yielding the value
    return dict(final_result)
