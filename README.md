# Unemployment Data Viz with an API

> Goal: To build an interactive data visualization that relies on a dynamic API backed by cloud services.

The tutorial will walk you through the process of creating a Vega-Lite chart that shows unemployment rates over time for a given county. The app allows the user to supply name of a county and state; once submitted, the app calls a custom API built with a Google Cloud Function. In turn, this cloud function runs a SQL query on a BigQuery data table containing county-level data from the Bureau of Labor of Statistics.

- [Initial setup](docs/setup.md)
- [API - Hello World](docs/api_hello_world.md)
- [BLS data and GCP BigQuery](docs/bigquery.md)
- [API - BLA County Data](docs/api_bls.md)