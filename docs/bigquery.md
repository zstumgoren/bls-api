## Data in the Cloud 

In order to create a dynamic API, we'll need to store data in the cloud in a way that allows live querying.

The goal here is to allow our Cloud Function API to query for the unemployment data for a given county, and then return that data to the web app for display in a Vega-Lite chart. 

Data storage and querying is a big subject, and there are myriad ways to store and query data in the cloud. 

Sites/services often use relational databases such as Postgres or key-value stores such as Firebase to store data used by APIs and web applications.

These all pose some level of technical difficulty with respect to setup and usage. 

BigQuery is a simple option for storing and querying data on Google Cloud Platform. 

It can handle data of varying sizes with a fair degree of speed, and is quite easy to set up and use with basic CSVs.

## BigQuery Overview

Let's load up BigQuery

* Download the `bls_monthly_unemployment_by_county.csv`
* Create a new BLS dataset on BigQuery
* Create a table by uploading the BLS data:
  * Click the option dots next to `bls` and select `Create table`
  * Fill in the form as follows:
    * `Create table form` - Choose `Upload`
    * `Select file` - Browse local files to select `bls_monthly_unemployment_by_county.csv`
    * `Table` - Name the table `unemployment`
    * `Schema` - Check the box next to `Auto detect`. This will
      automagically identify data types for each column, such as string for county name and float for unemployment rate
  * Click `Create table`
* Review the data types for columns that were automatically inferred
* Craft some SQL queries that find counties in a state and data points for a specific county:

*Locate your county.*

```
SELECT DISTINCT `county`, `state`, `area`
FROM `hs-research-tumgoren.bls.umemployment`
WHERE `county` LIKE 'Marin County'
;
```

*Find data for your county.*

```
SELECT * FROM `hs-research-tumgoren.bls.umemployment` 
WHERE `county` = 'Marin County' and `state` = 'CA'
;
```

Other SQL queries for tinkering:

* Counties with highest and lowest unemployment rates?
* Largest counties with highest/lowest unemployment?
* Counties sorted by labor force