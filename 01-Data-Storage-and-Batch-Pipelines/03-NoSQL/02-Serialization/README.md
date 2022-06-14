# Exercise 1 - Serialization formats

In this exercise we are going to explore the following data exchange formats:

Text-based:
- CSV: Comma-separated values, the simplest of the day
- JSON: Javascript Serialization Object Notation

XML:
- Excel files
- HTML files

Binary:
- Protobuf
- Pyarrow
- Postgres wire protocol.

## 1.a World bank - rural population

Let's download data from [the World Bank](https://data.worldbank.org/indicator/SP.RUR.TOTL.ZS?view=chart) about rural population, in Excel format.

We are going to use `wget` to download this data. Create a data `/datasets` directory using the command line and download the dataset in Excel format using `wget`, name the file `wb-rural.xls`.

$CHA_BEGIN
`wget -O wb-rural.xls 'https://api.worldbank.org/v2/en/indicator/SP.RUR.TOTL.ZS?downloadformat=excel'`
$CHA_END

Track
- Open the dataset with Pandas and OpenPyxl
- List the name of the Excel sheets
- Download a second dataset about [forest area](https://data.worldbank.org/indicator/AG.LND.FRST.ZS?view=chart)
- Return the countries with the largest amount of forest area
- Return the countries with the largest ratio of forest area by number of inhabitants in rural area.
- Write a protobuf schema for both datasets merged
- Write a Parquet schema for the datasets and store them in Parquet files, notice the file size difference
