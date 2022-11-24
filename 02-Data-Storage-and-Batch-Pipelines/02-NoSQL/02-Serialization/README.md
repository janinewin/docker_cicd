### Introduction

In this exercise we are going to explore several data exchange formats. They're different ways to store and share the same data. They all have pros and cons.

Let's start with a bit of reading 📖 !

---

### Text-based formats 📜

#### CSV: Comma-separated values

The simplest of the day. Take a look at the [CSV Wikipedia page](https://en.wikipedia.org/wiki/Comma-separated_values) and read the section `Basic rules`.

On [Kaggle > Datasets](https://www.kaggle.com/datasets), there are many public CSV datasets. Using the `Filters` feature, **find one and use the online `Data Explorer` section of the dataset** to look at the CSV's characteristics.

<details>
  <summary markdown='span'>💡 Hint</summary>

  For example, open [Netflix TV Shows and Movies here](https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies): scroll to the "Data explorer" section and look at the Detail / Compact / Column breakdown.
</details>

#### JSON: Javascript Serialization Object Notation.

Probably the most common format for web APIs. Take a look at the syntax on the [JSON Wikipedia page](https://en.wikipedia.org/wiki/JSON), `Syntax` section.

On [Kaggle > Datasets](https://www.kaggle.com/datasets), using the `Filters` feature, find a JSON dataset and use the online `Data Explorer` section.

<details>
  <summary markdown='span'>💡 Hint</summary>

  The [Engagement and job fit of retail salespeople](https://www.kaggle.com/datasets/pmenshih/retail-chain-salespeople-engagement) is an example, scroll to "Data explorer".
</details>

Note how different the `Data explorer` looks. **Why do you think that is?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  CSVs are rectangles, while JSONs are trees. Their fundamental shape is different and therefore we can't model or visualize data in the same fashion using either of them.
</details>

#### XML: Extensible Markup Language

Here is a snippet of XML

```xml
<xs:element name="name">
  <xs:complexType>
    <xs:sequence>
      <xs:element name="name">
        <xs:simpleType>
          <xs:restriction base="xs:string"></xs:restriction>
        </xs:simpleType>
      </xs:element>
    </xs:sequence>
  </xs:complexType>
</xs:element>
```

Similarly to JSON, XML can express tree-like data structures.

**What's a common file format, used on web pages, that looks like a cousin of XML?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  It starts with an H like Hypertext...
</details>

XML is still used by some websites, but admittedly rarely, we won't dive too much into it.

Take a look at this [official JSON page example](https://json.org/example.html).

```json
{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}
```

Right below it, you'll find the same data expressed as XML

```xml
<!DOCTYPE glossary PUBLIC "-//OASIS//DTD DocBook V3.1//EN">
<glossary><title>example glossary</title>
  <GlossDiv><title>S</title>
    <GlossList>
      <GlossEntry ID="SGML" SortAs="SGML">
        <GlossTerm>Standard Generalized Markup Language</GlossTerm>
        <Acronym>SGML</Acronym>
        <Abbrev>ISO 8879:1986</Abbrev>
        <GlossDef>
          <para>A meta-markup language, used to create markup
      languages such as DocBook.</para>
          <GlossSeeAlso OtherTerm="GML">
          <GlossSeeAlso OtherTerm="XML">
        </GlossDef>
        <GlossSee OtherTerm="markup">
      </GlossEntry>
    </GlossList>
  </GlossDiv>
</glossary>
```

**Which one is more verbose?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  More verbose = more text to express the same idea.
</details>

**Remember the basic data structures in Python, what does this JSON snippet look like?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  If you do `a = {"hello": "world"}` in Python, what's the type of `a`?
  Try `type(a)` to get the answer.
</details>

---

### Binary formats 🤓

Contrary to text-based formats, which are human-readable, binary formats aren't, but tend to be much more compact, and computer-friendly. We'll explore three formats here.

#### 1. Protobuf, the one standard for Google data

Did you know that all of Google Cloud APIs send data as Protobufs? That's because Google developed it.

Read the [introduction to Protocol Buffers (aka Protobuf)](https://developers.google.com/protocol-buffers) and note 2 things:

1. Messages are typed beforehand.
2. Code needs to be generated in your language of choice before being able to use a Protocol buffer.

To read a JSON file in Python, we can do

```python
import json

json.load(...)
```

Literally any JSON file can be parsed, its fields and structure do **not** need to be known in advance. We compromise speed and size of the message for readability and flexibility.

**In Protobuf, based on [this section](https://developers.google.com/protocol-buffers/docs/pythontutorial#compiling-your-protocol-buffers), can we do?**

```python
import protobuf

protobuf.load(a_protobuf_file)
```

<details>
  <summary markdown='span'>💡 Hint</summary>

  Why would we compile code if we can just load it generically?
</details>

Protobuf requires you to
- know the data format beforehand
- compile code against the data format (or schema), which are these `.proto` files defining the `message ... { ... }`

We compromise readability and ease of use to optimize for speed and message size. The exact opposite of JSON in this case.

#### 2. Parquet files 🪵

The following analogies are a little far fetched, but still fair:
- Protobufs are the "binary, compiled equivalent" of JSON
- Read this brief and [great introduction to Parquet](https://databricks.com/fr/glossary/what-is-parquet) by Databricks. **What do you think Parquet files are the binary equivalent of?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  They're rectangular, and the main data structure in Pandas.
</details>

In particular, look at the ridiculous comparison of data size, query run time and cost of CSVs vs. Parquet files. Worth the extra effort isn't it?

#### 3. Carpet files 🃏

It's a joke with `parquet`. Floor tile files don't exist either.
Sorry.

---

### Summary of text vs binary file formats

Text formats are typically more ✅ **human-readable** and **flexible** to work with, at the expense of ❗️ **compute speed** and **disk / memory** space usage.
Binary formats are ❗️ **not human-readable** and usually less flexible (even though libraries are great nowadays), but ✅ are more efficient for computers on typically all metrics. They're a bit harder to use at first but will end up saving you 💲.

## Let's play with real data!

In this exercise, we'll explore the [rural population dataset](https://data.worldbank.org/indicator/SP.RUR.TOTL.ZS?view=chart) from the World bank, as a percentage of total population, over time, by country.

**Do a quick [browse of the accessible data](https://data.worldbank.org/) from the World Bank**. How amazing is it to have all this public data at our fingertips 🤓?

### 1. Download the data

Back to our [rural population dataset](https://data.worldbank.org/indicator/SP.RUR.TOTL.ZS?view=chart), let's download it and explore it.

**First, get the CSV data file path from the browser**

<details>
  <summary markdown='span'>💡 Hint</summary>

  On the right hand side, check "Download", then right click and "Copy link address" (on Chrome).
</details>

Now on VSCode, open a terminal in this exercise's directory and use `wget` to download the file. Even if you're a `wget` pro, open the following hint to discover a powerful tool pre-installed on your server.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Ever heard of `man`? The manual on Linux. See the [command usage](https://en.wikipedia.org/wiki/Man_page). You can try `man wget`.
  Not very user friendly is it?
  We've also installed [tldr](https://github.com/tldr-pages/tldr), which you can think of as a `man` for the 21st century. Try `tldr wget`.

  The command is `wget -O worldbank-rural.zip 'https://api.worldbank.org/v2/en/indicator/SP.RUR.TOTL.ZS?downloadformat=csv'`
</details>

Once the zip downloaded, move it to a data directory and unzip it.

```
mkdir -p ./data/
mv /path/to/your/zip ./data/
unzip ./data/*.zip -d ./data
```

Now in VSCode you should see all the CSVs showing up. The file names are a bit hard to read, we mostly care about the one starting with `API`. Rename it to `API-rural.csv` from the terminal.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Use the `mv` command. Don't know how? Try Try `tldr mv`.
</details>

Run `make test`, the first test should pass.

### 2. Discover the Python packages we'll use

Open the `pyproject.toml` file. We use Poetry for Python packages management. If you haven't already, [read up about the pyproject.toml file](https://python-poetry.org/docs/pyproject/). In this exercise, we care mostly about these two lines:

```toml
pandas = "^1.4.2"
pyarrow = "^8.0.0"
```

We'll install the [pandas](https://pandas.pydata.org/) package to deal with tabular data (like CSVs) and [pyarrow](https://arrow.apache.org/docs/python/index.html) to deal with Parquet files.

### 3. Clean up the CSV

A bit of cleanup is unfortunately necessary, look at the first lines of the file.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Type `head /path/to/API-rural.csv`.
</details>

**What do you notice?**

The first lines are some of the CSV's documentation. That's a **very wrong** design by the World bank data engineers here 😱! But that's the way "real world data" is. Manually cleaning is always necessary, as we'll see throughout the bootcamp.

If you feel solid with the command line, remove the first few lines programatically (see the hint below). Otherwise, simply open the file `data/API-rural.csv` in VSCode and remove the lines by hand, until the column titles `"Country Name","Country Code",...`.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Check out this [StackOverflow](https://stackoverflow.com/a/339941) answer about removing the first few lines.
</details>


### 4. Load it with Pandas

In the file `lwserialization/rural.py`, let's import the Pandas library.

<details>
  <summary markdown='span'>💡 Hint</summary>

  You'd import `pandas` the same way you import any other library.
  There's an example on the [Pandas > Getting started](https://pandas.pydata.org/getting_started.html).
</details>

Fill out the function `load_rural_csv` to load the DataFrame. Feel free to open a IPython interactive shell to try this out. Type `ipython` in your directory, then `import pandas`, and try to load the DataFrame.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Same hint as the previous one, the [Pydata Pandas doc](https://pandas.pydata.org/docs/) is your friend. Google "Pandas read csv" and look for the answer within the Pydata website.
</details>

Now look at the columns of the DataFrame. Open the IPython interactive shell to try this out. Type `ipython` in your directory, then `import pandas`, and try to load the DataFrame.

Now, to load the DataFrame in a variable, type:

```python
from lwserialization import rural

df = rural.load_rural_csv()
```

Let's explore the dataset a bit, answer the following questions, by typing the answers in the code, fill in the return value of the associated functions.

- How many rows does the dataset have?  Fill `def explore_size():`.
- How many columns? Fill `def explore_columns():`
- How many countries are in the dataset? Fill `def explore_countries():`

### 5. Save it to the Parquet data format

Now that we have a function to load the CSV as a `pandas.DataFrame`, we'll save it to the Parquet data format to try and optimize for disk usage 💾.

Fill the `dataframe_to_parquet(...)` function taking as input a `pandas.DataFrame` and a filepath, and storing it to disk.

<details>
  <summary markdown='span'>💡 Hint</summary>

  The Parquet documentation helps you [here](https://arrow.apache.org/docs/python/parquet.html#reading-and-writing-single-files).
</details>

Notice the intermediate conversion needed between a `pandas.DataFrame` and a `pyarrow.Table`.

**Now run this function on the CSV file, do we save space?**

Store the file under `data/API-rural.parquet`.

<details>
  <summary markdown='span'>💡 Hint</summary>

  - Open a IPython terminal with `poetry run ipython`
  - To autoreload your Python code, you can add and evaluate the two following cells, [like described here](https://ipython.org/ipython-doc/3/config/extensions/autoreload.html)
    - `%load_ext autoreload`
    - `%autoreload 2`
  - The apply the sequence of functions that make the most sense, by now you've written them all! Answer in the second hint if you need ⬇️
</details>

<details>
  <summary markdown='span'>💡 Hint</summary>

  - Import the `rural` library
  - Load the DataFrame with `rural.load_rural_csv`
  - Call the `rural.dataframe_to_parquet` function, pass it the DataFrame and `./data/API-rural.parquet`.
</details>

Maybe it seems like nothing, but this last function is a proper data pipeline! We've loaded data in its original format and converted it to a binary, more efficient format, for further use and processing. 🎆
