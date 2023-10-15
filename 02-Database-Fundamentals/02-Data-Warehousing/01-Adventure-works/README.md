## Setup the data

AdventureWorks is a full database example provided by Microsoft and representing a made up bike company AdventureWorks Cycles. We will begin by uploading the data to Big Query and then work on creating some usable data marts!


### Download the data

First, we will download the data from the Microsoft Github repository.

```bash
wget https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks-oltp-install-script.zip
```

Create a data folder and unzip the data into it

```bash
mkdir -p data/original && unzip AdventureWorks-oltp-install-script.zip -d data/original
```

The formatting of some of the CSVs is not ideal for u. Luckily, there is a script to convert the CSVs to a more usable format.

```bash
mkdir -p data/processed && python pipeline/process_csvs.py
```

We are going to focus primarily on sales to limit ourselves. There is one CSV that is not quite right. Check out
`data/processed/store.csv`, what do you think is wrong with it?

<details>
<summary markdown='span'>Hint</summary>

The fourth column is XML, which is not that useful to us! We will need to fix this before we can upload the file to Big Query.

</details>

### 🔨 Fix store!

Checkout the `pipeline/process_store.py`

1. Fix `parse_xml_to_dict`. There is an example for you to test it on in the `__main__` function. You can check how the function is working using the `__main__` block, which should output a dictionary with keys and values. Try using the imported ET module.

<details>
<summary markdown='span'>Processed dictionary</summary>

{'{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}AnnualSales': '3000000', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}AnnualRevenue': '300000', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}BankName': 'Primary Bank & Reserve', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}BusinessType': 'OS', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}YearOpened': '1974', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Specialty': 'Mountain', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}SquareFeet': '75000', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Brands': '2', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Internet': 'T1', '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}NumberEmployees': '93'}

</details>


2. Update `main` to use the `parse_xml_to_dict` function. You should create a new store to CSV with the outfile, add each of the values from the dict as columns at the end of the CSV and remove the XML column!

3. Update the `__main__` block to run the `main` function and check that the output CSV looks correct!

The first row should look like this:

```csv
292	Next-Door Bike Store	279	A22517E3-848D-4EBE-B9D9-7437F3432304	2014-09-12 11:15:07.497000000	800000	80000	United Security	BM	1996	Mountain	21000	2	ISDN	13
```

### Create tables

Let's create a raw dataset to put our data in before moving to data processing and creating our Mart!

1. Create a dataset called `raw` in the EU region using `bq`

<details>
<summary markdown='span'>💡 Solution</summary>

```bash
bq --location=EU mk --dataset raw
```

</details>

2. Checkout the `pipeline/schemas.py`. You should see the schema for all of the tables, describing the columns they contain. Now that the store is fixed, they are related to sales now. However we still need to make some editing to add the new columns from the XML edit!

<details>
<summary markdown='span'>💡 Completed store schema</summary>

```
    "Store": [
        {"name": "BusinessEntityID", "type": "INT64", "mode": "REQUIRED"},
        {"name": "Name", "type": "STRING", "mode": "REQUIRED"},
        {"name": "SalesPersonID", "type": "INT64", "mode": "NULLABLE"},
        {'name': 'rowguid', 'type': 'STRING', 'mode': 'REQUIRED'},
        {"name": "ModifiedDate", "type": "TIMESTAMP", "mode": "REQUIRED"},
        {"name": "AnnualSales", "type": "FLOAT64", "mode": "REQUIRED"},
        {"name": "AnnualRevenue", "type": "FLOAT64", "mode": "REQUIRED"},
        {"name": "BankName", "type": "STRING", "mode": "REQUIRED"},
        {"name": "BusinessType", "type": "STRING", "mode": "REQUIRED"},
        {"name": "YearOpened", "type": "INT64", "mode": "REQUIRED"},
        {"name": "Specialty", "type": "STRING", "mode": "REQUIRED"},
        {"name": "SquareFeet", "type": "INT64", "mode": "REQUIRED"},
        {"name": "Brands", "type": "STRING", "mode": "REQUIRED"},
        {"name": "Internet", "type": "STRING", "mode": "REQUIRED"},
        {"name": "NumberEmployees", "type": "INT64", "mode": "REQUIRED"},
    ],
```

</details>

3. We want to create the tables using the schemas

❓ Complete the inside of the loop of `main` inside `pipeline/create_tables.py` to create the tables using the schemas!

Once that is completed, you can run the script and checkout the created table in Big Query!

### Upload the data

Now that we have all the data, we want to add it to the tables!

1. Checkout the `pipeline/upload_data.py`. You should see the `main` function has a loop that iterates over the tables and uploads the data to the table.

2. ❓ Complete the loop to upload the data to the tables!

3. Run the script and check the data is in the tables!


### Query the data

Now that we have the data in the table, we can start to query it!

```
bq query "SELECT * FROM raw.Store LIMIT 10;"
```

### 🏁 Finished

Now we have the data in Big Query, we are all ready to create our data marts in the next exercise!
