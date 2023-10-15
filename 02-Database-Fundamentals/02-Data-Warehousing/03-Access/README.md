## Access

So now we have a data mart. Next step is to give an analyst access to it.

### Features of the view

### Business Context for the View

❓ Create a view called `AnalystSalesView`

1. **Sales Performance**: Details like `OrderQty`, `UnitPrice`, and `LineTotal` help in analyzing the revenue streams.
2. **Promotion Effectiveness**: By including `SpecialOfferDescription` and `SpecialOfferDiscount`, analysts can measure the impact of various promotions on sales.
3. **Temporal Trends**: The sales date and year (`SalesOrderDate`, `SalesOrderYear`) enable trend analysis over time.
4. **Regional Analysis**: The inclusion of `TerritoryName`, `TerritoryCountry`, and `TerritoryGroup` allows for region-specific sales analysis.

Once you have created this view

### GCP IAM Permissions

To provide analysts with permission to query this view in GCP, you can set up IAM roles in Google Cloud Platform. You can grant the role of `roles/bigquery.dataViewer` specifically for the dataset and the view.

❓ Look up how to do this in the [GCP documentation](https://cloud.google.com/bigquery/docs/dataset-access-controls#bigquery-dataset-iam-roles) and do it via the cli to give access to a class mate


Check that they can query your view and nothing else!

### Saving money

❓ How can we save money on this view?

<details>
<summary markdown='span'>💡 Answer</summary>

We can make it materialized and schedule it to refresh overnight everyday!

</details>


❓ First create the materialized view


❓ Create a scheduled query to refresh the view every night at 3am

<details>
<summary markdown='span'>💡 Refresh query</summary>

```sql
ALTER MATERIALIZED VIEW sales_mart.AnalystMaterializedView
REFRESH;
```
