## Overview

Creating a search feature backed by a REST API using Google Cloud services.
Provides a wo

Different versions of the site demonstrate varying techniques for
controlling access to the back-end.

* [bls-api/open](https://zstumgoren.github.io/bls-api/open/) - Use CORS to allow API requests from any origin. Cloud Function set up to *allow unauthorized requests*.
* [bls-api/cors](https://zstumgoren.github.io/bls-api/cors/) - Use CORS to *restrict* API resquests from browsers based on a specific domain. Cloud Function set up to *allow unauthorized requests*. **This still allows non-browser requests!**
* [bls-api/apikey](https://zstumgoren.github.io/bls-api/cors/) - Uses an API Key tied to a specific domain to restrict access based on domain?


```
# This still works on the cors version
curl -m 70 https://us-west2-hs-research-tumgoren.cloudfunctions.net/bls_cors\?county\=Marin%20County\&state\=CA
-H "Content-Type:application/json"
```

Test default helloworld cloud function.

```bash
curl --header "Content-Type: application/json" \
     --request POST \ 
     -d '{"name":"ayla"}' \
     https://us-west2-hs-research-tumgoren.cloudfunctions.net/hello_world
```

## Overview

- BigQuery
- Cloud Functions

## Setup

* Create GCP account
* Enable APIs
 * Cloud Function
 * BigQuery

## BigQuery sample data

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

## REST API

### Setup and test

* Refresher on APIs. Introduction of REST
* Create a hello world API using [Cloud Function](https://developers.google.com/learn/topics/functions) based on [basic docs](https://cloud.google.com/functions/docs/create-deploy-http-python)
  * Go to IAM and grant your user the Cloud Functions Admin role. This
  will be required to create a public (unauthenticated) HTTP REST endpoint.
  * Create a hellow world Cloud Function to test the service. Select the
  `Allow unauthenticated invocations` option during creation.
  * Select Python 3.9
  * Deploy the default code for hello_world
* Test the new endpoint
  * Go to the `Trigger` tab and copy the `Trigger URL`
  * Test the query by pasting the URL into your browser, first with no
    argument, then with an argument (e.g. `message=howdy world`).

> Use curl and/or Python to demonstrate API usage and results?

### Dynamic BLS query

* Click `Edit` to update the function
* Add `google-cloud-bigquery` to `requirements.txt`
* Per the instructions for the [python bigquery client][], update `main.py` to import the library and perform a basic query of the BLS data using a static SQL query.

```
import json
from google.cloud import bigquery

client = bigquery.Client()


def hello_world(request):
    query = """
        SELECT *
        FROM `hs-research-tumgoren.bls.umemployment`
        WHERE `county` = 'Marin County' and `state` = 'CA'
    ;
    """
    query_job = client.query(query)  # Make an API request.
    payload = {}
    for row in query_job:
        # Row values can be accessed by field name or index.
        payload.update({
            'area': row['area'],
            'county': row['county'],
            'state': row['state'],
        })
    return json.dumps(payload)
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
    """
```

## Create a new function

Now that we've proven we can connect to BigQuery from a Cloud Function,
let's create a new function so that we can name things properly.

Go to the area listing the cloud functions in the web console. On the
far right of the `hello world` function, select `Copy` to create a new
function based on the example code we have so far.

In the new function's Edit mode, change the `Function name` to `bls_county_data`.

Once again, select `Allow unauthenticated invocations`.

Save the configuration. Copy the new `Trigger URL`, which should have
`bls_county_data` at the end.

Click `Next` and update the code as below. These changes will:

- check for county and state parameters in the URL and
- dynamically build the query based on input via the URL

It will return a helpful suggestion if the correct parameters were not supplied.

Once the changes are made, click `Deploy` and wait for the function to be deployed. It is complete when you see a green circle with a check mark next to its entry in the Cloud Functions area in the web console. This usually takes a few minutes.

```
import json
from google.cloud import bigquery

client = bigquery.Client()


def bls_county_data(request):
    request_json = request.get_json()
    if request.args and 'county' in request.args and 'state' in request.args:
        # NOTE: You could do additional sanity checking and standardization here
        # on incoming data here
        county = request.args.get('county')
        state = request.args.get('state').strip().upper()
    else:
        return f'You must supply the county and state URL parameters'
    query_template = """
       SELECT *
       FROM `hs-research-tumgoren.bls.umemployment`
       WHERE `county` = '{}' and `state` = '{}'
    ;
    """
    query = query_template.format(county, state)
    query_job = client.query(query)
    payload = {'data':[]}
    for row in query_job:
        # Row values can be accessed by field name or index.
        payload.update({
            'area': row['area'],
            'county': row['county'],
            'state': row['state'],
        })
        payload['data'].append({
          'month_abbrev': row['month_name'],
          'month': row['month'],
          'year': row['year'],
          'civ_labor_force': row['civ_labor_force'],
          'employed': row['employed'],
          'unemployed': row['unemployed'],
          'unemployed_rate': row['unemployed_rate'],
        })
    return json.dumps(payload)
```

Now we should test the new function.

First, get the `Trigger URL` and call it without any parameters.This should return our error message

Next, supply the correct URL parameters, e.g.`?county=Marin County&state=CA`. The query should work this time.


[python bigquery client]: https://cloud.google.com/bigquery/docs/reference/libraries#using_the_client_library


## Debugging Cloud Functions

Update the Cloud Function to print county and state info and then raise an Exception with a custom message.

Trigger the updated API endpoint and then view the logging and traceback info in the function's `Logs` section in the web console.


## Set the content type

Update the Clouf Function to return `application/json` in request headers.

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
