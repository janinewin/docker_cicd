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

- Inspiration from [this tutorial](https://nyu-cds.github.io/python-bigdata/02-mapreduce/)
- [MapReduce steps](https://cdn.educba.com/academy/wp-content/uploads/2020/04/map-flowchart.png.webp)

## Use Pyspark

- Inspiration from [this tutorial](https://nyu-cds.github.io/python-bigdata/03-spark/)

## Use Apache Beam

- Count words [example](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount.py)

## BONUS 🤝. Beam on Google Cloud

- Transform the Beam code to run on [Google Dataflow](https://github.com/tuanavu/google-dataflow-examples/blob/master/examples/wordcount.py)
