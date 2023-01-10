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

❓ Let's implement a very basic counter in Python in `impl_python.py`, and use it as a baseline against other methods.

Run `make test` once done, the first two tests should pass.

# 2️⃣ Implement Map-Reduce purely in Python

As its name indicates, the Map-Reduce paradigm follows steps of either mapping or reducing.

We'll implement in Python the following steps, described on [this diagram](https://cdn.educba.com/academy/wp-content/uploads/2020/04/map-flowchart.png.webp).

<img src="https://cdn.educba.com/academy/wp-content/uploads/2020/04/map-flowchart.png.webp" width=600>

In the `lwmr/impl_mapreduce.py` file, you'll see one function for each of the steps. The function signatures and description will indicate you what the input looks like and what the output should be.

The key concept to understand in Map/Reduce is: we're looking for opportunities to parallelize our work. This means, whenever possible, we'll apply transformations that allow us to have multiple servers run computation (`map` steps). Once all servers are done, their results are coordinated and aggregated in a `reduce` phase.

**While word count is the most typical example to showcase Map/Reduce, its breakdown feels a bit convoluted 🐡**

## 2.1) Reasoning with types

Each step of the process takes a dataset in some shape as input, and transforms it to a new dataset in a new shape. Inputs have a specific type, outputs have another one.

Before writing any code, let's reason about each step's input and output types.

## 2.2) Let's work on the implementation, starting with `split_file_into_chunks`

- Inputs:
  * txt_path: `str`   -> path to large text file
  * nb_chunks : `int` -> number of sub-files to create (simulate HDFS chunks in separate nodes)
- Output:
  * `List[str]` -> list of file path for each chunk


Start with the `def split_file_into_chunks(...)` function.


## 2.3) From splitting to mapping

For each group of words, we'd like to apply a mapping function `def simple_map_word_to_word_and_one(...)` that has:

- Inputs: a single file path (for one chunk)
- Output: a list of couples (a tuple of size 2 in Python), where each couple is the word, and just 1. This gives us `List[Tuple[str, int]]`.

Now that we have the function for a single file, we'd like to apply it to all chunks. **⏩ In production, this would be done in parallel, and give us the huge performance benefits of Map / Reduce.**

The function `map_on_each_chunk` takes:

- Inputs: the list of paths for each chunk file, which is the output of the function `split_file_into_chunks(...)`, that's a `List[str]`
- Output: The result of the function `def simple_map_word_to_word_and_one(...)`, but for each chunk file, and that's a list of the output of that function. Still following 😄? So the final output is of type `List[List[Tuple[str, int]]]`.

**Fill in the `map_on_each_chunk` function**

## 2.4) From mapping to shuffling

Shuffling here is regrouping the groups, by word. The output will therefore be of the type:

- Output: `List[str, List[int]]`, a list where the first value is the word, and the second value is the list of all ones for that word from all previous groups.
- Inputs: as input, we pass the output of the mapping, that's easy we just wrote it above: `List[List[Tuple[str, int]]]`.

**Implement the `shuffle` function**

## 2.5) From shuffling to reducing

A reduce step always brings the dimension of the data down, think of it like <i>if we have a list of list as an input, we get a list as an output</i>.

Here, as inputs we have:

- Inputs: the output of the shuffling part which is a dictionary `Tuple[str, List[int]]`

And we'd like to return a final count for a specific word, which is a `Tuple[str, int]`.
The reduce function is a simple sum of all ones for a word, that is going to give the final **count for a word** 🎉

**Implement the `count_for_one_word` function, which is used then by the `final_reduce` function for every words**

# 3️⃣ Putting everything together

## 3.1) Single processing

**Implement the `count_words_mapreduce` function**

Here as inputs we have:

- Inputs: the list of paths of chunks

The ouput is ultimately the count of words going through the 3 steps: Map/Shuffle/Reduce


## 3.2) Multiprocessing

**Implement the `count_words_mapreduce_multiproc` function**

Here the input is the same

- Inputs: the list of paths of chunks

We have to think about to parralelize the work. We are lucky the bricks are already available.
Let's instantiate a pool of workers and map each single function
❗️ Not all steps are possible to parralelize

<details>
  <summary markdown='span'>💡 Hint</summary>

  The `shuffle`function part needs to gather all the words together it cannot run easily in multiple process

  `map_on_each_chunk` and `count_for_one_word` can be mapped over multiple workers

</details>

## 3.3) Compare both implementations

You can time the execution of all implementation and make sure to open a `htop` next to your terminal to see the parrallezation taking over all your cpu cores.
