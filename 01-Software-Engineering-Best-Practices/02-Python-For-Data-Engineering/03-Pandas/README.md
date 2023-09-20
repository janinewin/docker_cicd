# Pandas

Pandas is crucial for data engineering because it simplifies data manipulation, integration, exploration, and analysis. It offers powerful tools like DataFrames, which enable effortless cleaning, transforming, and reshaping of data. 🧹💪

Pandas seamlessly integrates multiple data sources and supports various file formats, facilitating data integration. 📂🔄

Handling missing data is made easier with pandas' methods for filling, dropping, or interpolating values. 📊🔍

The library provides statistical analysis, descriptive statistics, and data visualization functions for data exploration. 📈📉

By leveraging efficient data structures and operations, pandas improves computational speed and memory utilization. ⚡💾

Once data processing is complete, pandas allows for easy data export or integration with other tools or libraries. 📤🔧

Overall, pandas serves as a versatile tool for data engineers, boosting productivity and efficiency in their work. 🐼💻

## Data

We will use kaggle again this time to use this good reads [dataset](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews)

```
kaggle datasets download -d mohamedbakhet/amazon-books-reviews --unzip -p ./data
```

## Goal 🎯

We want to use pandas to build an example data pipeline we have our two csvs at the moment `books_data.csv` and `Books_rating.csv` The pipeline has these specifications beyond step 1 you can work in any order the exact instructions are included in all of the doc strings of the functions!

1. Complete `pandas_pipeline/load.py`
2. Complete `pandas_pipeline/best_books.py` to check the output is good run
```bash
pytest -k test_best_performing_books_csv
```
3. Complete `pandas_pipeline/category_distribution.py` to check the output is good run
```bash
pytest -k test_category_distribution_csv
```
4. Complete `pandas_pipeline/top_authors.py` to check the output is good run
```bash
pytest -k test_author_impact_analysis_csv
```
5. Complete `pandas_pipeline/review_years.py` to check the out is good run
```bash
pytest -k test_review_years_csv
```

## Finish 🏁

Once each of the functions work you can run the entire pipeline with

```bash
python pandas_pipeline/pipeline.py
```

and push the output of

```bash
make test
```
