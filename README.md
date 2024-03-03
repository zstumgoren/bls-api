# Unemployment Data Viz with an API

> Goal: To build an interactive data visualization that relies on a dynamic API backed by cloud services.

The tutorial will walk you through the process of creating a Vega-Lite chart that shows unemployment rates over time for a given county. The app allows the user to supply name of a county and state; once submitted, the app calls a custom API built with a Google Cloud Function. In turn, this cloud function runs a SQL query on a BigQuery data table containing county-level data from the Bureau of Labor of Statistics.

- [Initial setup](docs/setup.md)
- [API - Hello World](docs/api_hello_world.md)
- [BLS data and GCP BigQuery](docs/bigquery.md)
- [API - BLA County Data](docs/api_bls.md)

## Debugging Cloud Functions

Update the Cloud Function to print county and state info and then raise an Exception with a custom message.

Trigger the updated API endpoint and then view the logging and traceback info in the function's `Logs` section in the web console.


## Set the content type

Update the Cloud Function to return `application/json` in request headers.

## Create a basic search form that uses the API.

Create a simple page that uses JS to fetch the data and create a Vega Lite chart and some dynamic text.

## Locking down the API

TK Update the API to only work on a single domain, per the Cloud Function docs about setting CORS. It's possible we may need to create an API key and shift to authenticated mode in combination with a domain/origin restriction.

- Adding [CORS](https://cloud.google.com/functions/docs/writing/http#handling_cors_requests) support to non-auth Cloud Function

Is the above enough, or do we need to enable auth and then create an API key that is restricted to a domain?

## Tying it all together

* Restrict Cloud Function API by domain?
* Create GitHub pages site with index.html search feature that displays
  county-level unemployment data

Some features to include for county

- Search by county name
- Monthly unemployment rate chart:
  - Vega-Lite line chart for last 14 months
  - Caption with dynamic text stating current labor force, number
    unemployed, change since prior month and comparison to same month of prior year
  - On hover over month data point, show stats: Labor force, employed
    and unemployed counts

## Optimization Questions

Is this interactive project designed optimally?

How else could we approach the *architectural design*, especially given
that this data is limited in size and maps to a basic geographic entity
(i.e. county)?

Do we truly need this to be a dynamic search, even with the quantity of
data we have?