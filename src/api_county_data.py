"""
This file contains the code for the API endpoint that serves county-level unemployment data.
The endpoint is implemented as a Google Cloud Function that queries a BigQuery dataset and returns the results in JSON format.
"""
import functions_framework

from flask import jsonify, make_response
from google.cloud import bigquery

from werkzeug.datastructures import Headers


client = bigquery.Client()

@functions_framework.http
def county_data(request):
    county = request.args['county']
    state = request.args['state']

    query = (
    "SELECT county, state, date, unemployed_rate "
    "FROM `hs-research-tumgoren.bls3.unemployment` "
    "WHERE county = @county AND state = @state"
    )
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("county", "STRING", county),
            bigquery.ScalarQueryParameter("state", "STRING", state),
        ]
    )
    query_job = client.query(query, job_config=job_config)
   
    data = []
    for row in query_job.result():
      county = row['county']
      state = row['state']
      data.append({
          'date': row['date'].strftime('%Y-%m-%d'),
          'unemployed': row['unemployed_rate']
      })
    # Configure Headers
    # If you want to limit the allowed origins, 
    # you can replace '*' with a specific domain, e.g., 'https://example.com'
    headers = Headers()
    headers.add('Access-Control-Allow-Origin', '*')
    headers.add('Access-Control-Allow-Methods', 'GET')
    headers.add('Access-Control-Allow-Headers', 'Content-Type')
    headers.add('Access-Control-Max-Age', '300')
    resp = make_response(
      jsonify(
        county=county,
        state=state,
        data=data
      )
    )
    # ADD THIS line to include headers in response
    resp.headers = headers
    return resp
