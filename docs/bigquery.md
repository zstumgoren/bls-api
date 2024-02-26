## Data in the Cloud 

In order to create a dynamic API, we'll need to store data in the cloud in a way that allows live querying.

The goal here is to allow our Cloud Function API to query for the unemployment data for a given county, and then return that data to the web app for display in a Vega-Lite chart. 

Data storage and querying is a big subject, and there are myriad ways to store and query data in the cloud. 

Sites/services often use relational databases such as Postgres or key-value stores such as Firebase to store data used by APIs and web applications.

These all pose some level of technical difficulty with respect to setup and usage. 

BigQuery is a simple option for storing and querying data on the Google Cloud Platform. 

It can handle data of varying sizes with a fair degree of speed, and is quite easy to set up and use with basic CSVs. In particular, it allows you to write standard SQL queries against data that you've imported into the system.

### The BLS Data

The Bureau of Labor Statistics provides data on inflation, prices of goods and services, productivity and much more. They provide this data at varying aggregations such as nationwide and state levels.

For this tutorial, we're interested in the recent unemployment rate by county. BLS offers a "rolling" data set for the last 14-months on its [Local Area Unemployment Statistics](https://www.bls.gov/lau/tables.htm).

We're specifically interested in the file under the `County` section called [Labor force data by county, not seasonally adjusted, latest 14 months](https://www.bls.gov/web/metro/laucntycur14.txt).

Navigate to that page. You'll notice that the data is in a rather unfriendly format, at least for use with in a spreadsheet or similar tool.

Never fear, we'll handle that in the next step.

For now, right click and save the data to your local computer.

## Clean up the data

As mentioned, the BLS 14-month county data is not an ideal format for our purposes.

Now that you've downloaded the data, you can use the [clean_bls_unemployment_data.py](..scripts/clean_bls_unemployment_data.py) script to generate a clean, standardized CSV.

Download the script to the same location where you saved the `laucntycur14.txt`. Then run the following command in the shell:

```bash
python clean_bls_unemployment_data.py
```
## Load BLS Data into BigQuery

Let's load our cleaned-up BLS data into BigQuery and get familiar with some of its features. 

* Create a new BLS dataset on BigQuery
* Create a table by uploading the BLS data:
  * Click the option dots next to `bls` and select `Create table`
  * Fill in the form as follows:
    * `Create table form` - Choose `Upload`
    * `Select file` - Browse local files to select `bls_monthly_unemployment_by_county.csv`
    * `Table` - Name the table `unemployment`
    * `Schema` - Check the box next to `Auto detect`. This will
      automatically identify data types for each column, such as string for county name and float for unemployment rate
  * Click `Create table`
* Review the data types for columns that were automatically inferred

## Query the data

Now you can craft SQL queries for the data. 

For example, to locate `Marin County`.

```sql
SELECT DISTINCT `county`, `state`, `area`
FROM `hs-research-tumgoren.bls.umemployment`
WHERE `county` LIKE 'Marin County'
;
```

And to select unemployment data for `Marin County`.

```sql
SELECT * FROM `hs-research-tumgoren.bls.umemployment` 
WHERE `county` = 'Marin County' and `state` = 'CA'
;
```

Other SQL queries for tinkering:

* Counties with highest and lowest unemployment rates?
* Largest counties with highest/lowest unemployment?
* Counties sorted by labor force