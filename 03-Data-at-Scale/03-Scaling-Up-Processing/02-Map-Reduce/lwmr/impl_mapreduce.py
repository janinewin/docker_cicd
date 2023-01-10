import time
from typing import Dict, List, Tuple
from multiprocessing import Pool, cpu_count

from lwmr.text_processing import get_words


num_jobs = cpu_count()

#$DELETE_BEGIN
def split_list(l_to_split, n_chunks):

    batch_size = len(l_to_split)//n_chunks
    return [ l_to_split[i*batch_size:(i+1)*batch_size] for i in range(n_chunks)]
#$DELETE_END

def split_file_into_chunks(txt_path,nb_chunks):
    '''
    Reads a large txt file and create many smallest files depending on the number of chunks
    '''

    #$CHALLENGIFY_BEGIN
    with open(txt_path) as f:
        txt_lines = f.readlines()
    l_chunks = split_list(txt_lines,nb_chunks)

    i=1
    l_path=[]
    for chunk in l_chunks:
        path_target = txt_path.replace(".txt",f"-{i}-{nb_chunks}.txt")
        l_path.append(path_target)
        with open(path_target,"w") as f:
            txt_lines = f.writelines(chunk)
        i+=1

    return l_path
    #$CHALLENGIFY_END


def simple_map_txt_file_to_word_and_one(txt_path) -> List[Tuple[str, int]]:
    """
    From a text file path, read its content and map each word to a tuple (word ,1)
    """

    with open(txt_path) as f:
        txt = '\n'.join(f.readlines())

    words = get_words(txt)

    return  [(word,1) for word in words]

def map_on_each_chunk(chunk_paths: List[str]) -> List[List[Tuple[str, int]]]:

    mapped_chunks = [simple_map_txt_file_to_word_and_one(chunk_path) for chunk_path in chunk_paths]


    return mapped_chunks

def shuffle(
    word_groups_with_counts: List[List[Tuple[str, int]]]
) -> List[Tuple[str, List[int]]]:
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
    for word_one_chunk in word_groups_with_counts:
        for word, count in word_one_chunk:
            # If this word has never been seen, add it to the clusters map
            #$CHALLENGIFY_BEGIN
            if word not in clusters_map:
                clusters_map[word] = []
            #$CHALLENGIFY_END
            # Add the entry count to this word's key in the clusters_map dictionary
            #$CHALLENGIFY_BEGIN
            clusters_map[word].append(count)
            #$CHALLENGIFY_END

    # To follow map / reduce conventions, return a list (or a map) where each entry is of the form
    # (key, [value1, value2, value3, ...]), equivalent to the list of items of clusters_map dictionnary
    #$CHALLENGIFY_BEGIN
    return list(clusters_map.items())
    #$CHALLENGIFY_END

def count_for_one_word(word_mapped: Tuple[str, List[int]]) -> Tuple[str, int]:
    """
    Given a word and a "silly" list of ones, return the word and its total count: (word, count)
    """
    total_count = 0
    word, counts = word_mapped
    # Fill the code below, given a list of individual counts from the various word groups
    # to return the total counts
    pass  # YOUR CODE HERE
    return word, total_count

def final_reduce(shuffled_words: List[Tuple[str, List[int]]]) -> Dict[str,int]:
    '''
    take a list of words with their list of ones and reduce it to a list of word with their count within the text
    '''
    #$CHALLENGIFY_BEGIN
    return dict([count_for_one_word(shuffled_word) for shuffled_word in shuffled_words])
    #$CHALLENGIFY_END


def count_words_mapreduce(txt_path_files: List[str]):

    mapped_chunks = map_on_each_chunk(txt_path_files)

    shuffled_words = shuffle(mapped_chunks)

    reduced = final_reduce(shuffled_words)

    return reduced


def count_words_mapreduce_multiproc(chunk_file_paths: List[str]):
    #$CHALLENGIFY_BEGIN
    with Pool(num_jobs) as pool_workers:
        mapped_chunks = pool_workers.map(simple_map_txt_file_to_word_and_one, chunk_file_paths)

        shuffled_list = shuffle(mapped_chunks)

        reduced_items = pool_workers.map(count_for_one_word, shuffled_list)
        #pool_workers.map returns a list of tuple, we need to transform it to a dictionnary
        reduced = dict(reduced_items)


    return reduced
    #$CHALLENGIFY_END

if __name__=='__main__':

    txt_file = "data/The_Data_Engineering_Cookbook.txt"

    txt_files = split_file_into_chunks(txt_file,64)

    #$DELETE_BEGIN

    print("👉Starting map-reduce single processing...")
    start = time.perf_counter()

    counts = count_words_mapreduce(txt_files)

    end = time.perf_counter()
    print(f"✅ Done in {end-start} seconds \n")


    print("👉Starting map-reduce  multi processing...")
    start = time.perf_counter()

    counts_multi = count_words_mapreduce_multiproc(txt_files)

    end = time.perf_counter()
    print(f"✅ Done in {end-start} seconds using {num_jobs} processes")
    #$DELETE_END
