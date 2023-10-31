# Word count

In the world of big data processing, the [divide and conquer](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) strategy is a must-know.

It works as follows:

- Datasets are split into smaller datasets ✂️.
- An intermediate algorithm is applied to each smaller dataset ⛏️.
- The results on each intermediate, smaller dataset are aggregated to make the final result 🔗.

The equivalent of the ["Hello, World!"](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) program for big data processing the the **word count problem**.

**Problem: we have a large book, and would like to compute the number of occurrences of each word**

Big data technology has evolved over the years. The APIs have gotten more developer friendly and powerful over the years. In this exercise, we'll implement several versions of the same algorithm, with a jump in history every time 📜.

For the book, we'll use [The Data Engineering Cookbook](https://www.darwinpricing.com/training/Data_Engineering_Cookbook.pdf) by [Andreas Kretz](https://www.linkedin.com/in/andreas-kretz/?originalSubdomain=de), CEO of [LearnDataEngineering.com](https://learndataengineering.com/).

We've extracted the text in a [text file you can download](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/The_Data_Engineering_Cookbook.txt)
and duplicated many times (just to make the computation heavy😅 ). You can store it under a `data/The_Data_Engineering_Cookbook.txt` directory.

# 1️⃣ Really basic Python

❓ Setup: Run `poetry install` to be sure to get latest versions as per lockfile.

❓ Let's implement a very basic counter in Python in `impl_python.py`, and use it as a baseline against other methods. Store your peformance in `perf.yml`

Run `make test` once done, the first two tests should pass. 

# 2️⃣ Implement Map-Reduce purely in Python

## 2.1) The big picture

As its name indicates, the Map-Reduce paradigm follows steps of either mapping or reducing.

We'll implement in Python the following steps, described on [this diagram](https://cdn.educba.com/academy/wp-content/uploads/2020/04/map-flowchart.png.webp).

<img src="https://cdn.educba.com/academy/wp-content/uploads/2020/04/map-flowchart.png.webp" width=600>

👉 In the `lwmr/impl_mapreduce.py` file, you'll see one function for each of the steps. The function signatures and description will indicate you what the input looks like and what the output should be.

**The code flow is presented below**

```python
N_CHUNK = 64 # Suggested split number to use for the cookbook dataset
txt_path = "data/The_Data_Engineering_Cookbook.txt"

# 0. SPLITTING 
txt_files_paths = split_file_into_chunks(txt_path, n_chunk)
# --> Returns 64 paths to 64 small text files saved to disk, simulate HDFS chunks in separate nodes

# 1. MAPPING
mapped_chunks = map_on_each_chunk(txt_path_files)
# --> 64 lists of lists like [(Car, 1),(Car, 1),(River,1), ...]

# 2. SHUFFLING
shuffled_words = shuffle(mapped_chunks)
# --> 1 big list of tuples: e.g [('Car', [1, 1]), ('River', [1]), ...]

# 3. REDUCING
reduced = final_reduce(shuffled_words)
## --> 1 big dict of words: e.g. {'Car': 2, 'River': 1}
```

> While word count is the most typical example to showcase Map/Reduce, its breakdown feels a bit convoluted, it's normal! 🐡

The key concept to understand in Map/Reduce is: we're looking for opportunities to parallelize our work. This means, whenever possible, we'll apply transformations that allow us to have multiple servers run computation (`map` steps). Once all servers are done, their results are coordinated and aggregated in a `reduce` phase.
  
## 2.2) Implementation

### Splitting - implementing `split_file_into_chunks`

💡 For debugging purposes, we advise you to start with creating a very small text file made of only with few sentences, and `N_CHUNK=2`. It will make it faster and smaller to print & debug.

### Mapping - Implement `map_on_each_chunk` 

The function `map_on_each_chunk` takes:

⏩ In production, this would be done in parallel, and give us the huge performance benefits of Map / Reduce !

### Shufflinng - Implement `shuffle`

Shuffling here is regrouping the groups, by word. 

### Reducing - Implement `count_for_one_word`

The reduce function is a simple sum of all "ones" for a word, that is going to give the final **count for a word** 🎉


# 3️⃣ Putting everything together

## 3.1) Single processing

**Implement the `count_words_mapreduce` function**

Here as inputs we have:

- Inputs: the list of paths of chunks

The ouput is ultimately the count of words going through the 3 steps: Map/Shuffle/Reduce


## 3.2) Multiprocessing

**Implement the `count_words_mapreduce_multiproc` function**

- You'll have to instantiate a pool of workers and map each single function
- You'll have to think about how to parallelize the work. 
- Not all steps are possible to parallelize
- Most of the bricks of code are already available, but do refactor if you see some code re-used twice!


<details>
  <summary markdown='span'>💡 Hint</summary>

  The `shuffle` function part needs to gather all the words together it cannot run easily in multiple process

</details>

## 3.3) Compare both implementations

You can time the execution of all implementation and make sure to open a `htop` next to your terminal to see the parallel taking over all your cpu cores.
