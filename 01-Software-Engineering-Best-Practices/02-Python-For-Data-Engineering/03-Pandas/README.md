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

We want to use pandas to build an example data pipeline we have our two csvs at the moment `books_data.csv` and `Books_rating.csv` The pipeline has these specifications

1.
