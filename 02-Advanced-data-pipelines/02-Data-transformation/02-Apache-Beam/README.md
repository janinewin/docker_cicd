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

We've extracted the text in a [text file you can download](https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/data-engineering-cookbook-book/The_Data_Engineering_Cookbook.txt) under a `data/` directory here.

## Really basic Python

Let's implement a very basic counter in Python, and use it as a baseline against other methods.

<details>
  <summary markdown='span'>💡 Hint</summary>

  You can use the [Counter](https://docs.python.org/3/library/collections.html#counter-objects) in the standard library. There is a handy example.
</details>

Run `make test` once done, the first two tests should pass.

## Implement Map-Reduce purely in Python

As its name indicates, the Map-Reduce paradigm follows steps of either mapping or reducing.

We'll implement in Python the following steps, described on [this diagram](https://cdn.educba.com/academy/wp-content/uploads/2020/04/map-flowchart.png.webp).

<img src="https://cdn.educba.com/academy/wp-content/uploads/2020/04/map-flowchart.png.webp" width=400>

In the `lwmr/impl_mapreduce.py` file, you'll see one function for each of the steps. The function signatures and description will indicate you what the input looks like and what the output should be.

The key concept to understand in Map/Reduce is: we're looking for opportunities to parallelize our work. This means, whenever possible, we'll apply transformations that allow us to have multiple servers run computation (`map` steps). Once all servers are done, their results are coordinated and aggregated in a `reduce` phase.

**While word count is the most typical example to showcase Map/Reduce, its breakdown feels a bit convoluted 🐡. It's normal that some functions, like `simple_map_word_to_word_and_one` feel useless the first time.**

### Reasoning with types

Each step of the process takes a dataset in some shape as input, and transforms it to a new dataset in a new shape. Inputs have a specific type, outputs have another one.

Before writing any code, let's reason about each step's input and output types.

### Let's work on the implementation, starting with `split_words_into_groups`

- Inputs: list of words: `List[str]`
- Output: groups, where each group is a list of word `List[str]`. "groups" are lists as well, so that's `List[List[str]]`

Start with the `def split_words_into_groups(...)` function.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Try Numpy's [array_split](https://numpy.org/doc/stable/reference/generated/numpy.array_split.html).
</details>

### From splitting to mapping

For each group of words, we'd like to apply a mapping function `def simple_map_word_to_word_and_one(...)` that has:

- Inputs: a list of words `List[str]`
- Output: a list of couples (a tuple of size 2 in Python), where each couple is the word, and (yes it's a bit silly) just 1. This gives us `List[Tuple[str, int]]`.

Now that we have the function for a single group, we'd like to apply it to all groups. **⏩ In production, this would be done in parallel, and give us the huge performance benefits of Map / Reduce.**

The function `map_on_each_group` takes:

- Inputs: the list of each group, which is the output of the function `split_words_into_groups(...)`, that's a `List[List[str]]`
- Output: The result of the function `def simple_map_word_to_word_and_one(...)`, but for each group, and that's a list of the output of that function. Still following 😄? So the final output is of type `List[List[Tuple[str, int]]]`.

**Fill in the `map_on_each_group` function**

### From mapping to shuffling

Shuffling here is regrouping the groups, by word. The output will therefore be of the type:

- Output: `Dict[str, List[int]]`, a dictionary where the key is the word, and the value is the list of all ones for that word from all previous groups.
- Inputs: as input, we pass the output of the mapping, that's easy we just wrote it above: `List[List[Tuple[str, int]]]`.

### From shuffling to reducing

A reduce step always brings the dimension of the data down, think of it like <i>if we have a list of list as an input, we get a list as an output</i>.

Here, as inputs we have:

- Inputs: the output of the shuffling part which is a dictionary `Dict[str, List[int]]`

And we'd like to return a final count for each word, which is a `Dict[str, int]`.

**Implement the `count_within_group` function, which is used by the `final_reduce` function**

## Use Apache Beam

We are going to implement the code from [the Word Count example](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount.py). Our code lies in `lwmr/impl_beam.py`.

Let's detail block by block what's happening by breaking down the function `def count_words(...)`.

The first block is quite uneventful, we set up a Beam pipeline with default option and create the output directory.

```python
# Set up the pipeline with default options
pipeline_options = PipelineOptions()
pipeline_options.view_as(SetupOptions).save_main_session = True

output_dir = "/tmp/beam-output/"
prefix_fn = "test-output.txt"
output_fps_prefix = os.path.join(output_dir, prefix_fn)
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
```

Interesting stuff starts with

```python
with beam.Pipeline(options=pipeline_options) as p:
```

**What does the `with` keyword do?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  Let me [Stack Overflow](https://stackoverflow.com/a/1369553) that for you!

  Essentially, when code exits the `with` block, the method `__exit__()` is called on the variable `p`.
  It's great for database connections, file handles, etc.
</details>

In Beam, we write pipelines. Data is transformed step by step. The first step is to read the file.

**Replace `lines=None` with Beam code that will read from the input file path**

<details>
  <summary markdown='span'>💡 Hint</summary>

  You'll want to use the `ReadFromText` method.
</details>

At the end of this block, we now have a step which yields an iterator returning lines. We need to transform the lines into words. For that, our friend `text_processing.get_words()` is needed.

**Based on the value of `words`, fill in `WordExtractingDoFn -> process()`**

Great, now we have an iterator of words. Let's count them. The steps are very similar to Map / Reduce!

```python
counts = (
    words
    | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
    | 'GroupAndSum' >> beam.CombinePerKey(sum))
```

As you can see, we start by mapping each word `x` to `(x, 1)`, which is itself, and 1.

**Next, what does `CombinePerKey` do?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  Check the [official doc](https://beam.apache.org/documentation/transforms/python/aggregation/combineperkey/)
</details>

Finally, we're ready to map the results and write them to disk.

```python
output = counts | 'Format' >> beam.MapTuple(format_result)

# We write the output to files with the prefix `output_fps_prefix`
output | 'Write' >> WriteToText(output_fps_prefix)
```

As we'd like our results in a dictionary, but Beam writes them to disk, we'll parse the output files into a dictionary. That's what `counts = read_results(output_dir, prefix_fn)` does.

**The results should be in `/tmp/beam-output/`, check out what's in there.**

🔱 BIM! Well done, you've written multiple times the Word Count algorithm. The Beam way is the most scalable, and super well integrated with the Google Cloud ecosystem. Since Beam is open source, you'll find Beam runners on most other available clouds.

## BONUS 🤝. Beam on Google Cloud

- Transform the Beam code to run on [Google Dataflow](https://cloud.google.com/dataflow/docs/quickstarts/create-pipeline-python?hl=en#run-the-pipeline-on-the-dataflow-service)
