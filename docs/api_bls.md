



```python
from flask import jsonify, make_response
from google.cloud import bigquery
from werkzeug.datastructures import Headers

client = bigquery.Client()

def county_data(request):
  # Set CORS headers for the preflight request
  if request.method == "OPTIONS":
      # Allows GET requests from any origin with the Content-Type
      # header and caches preflight response for an 3600s
      headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
      }
      return ("", 204, headers)
  # Handle request
  if request.args and 'county' in request.args and 'state' in request.args:
    county = request.args['county']
    state = request.args['state']
  else:
    return ('You must supply the county and state URL paramters', 204)
  query = (
    "SELECT * "
    "FROM `hs-research-tumgoren.bls.unemployment` "
    f"WHERE `county` = '{county}' and `state` = '{state}';"
  )
  query_job = client.query(query)
  data = []
  for row in query_job:
    area = row['area']
    county = row['county']
    state = row['state']
    data.append({
      'month_abbrev': row['month_name'],
      'date': f"{row['year']}-{row['month']}-01",
      'civ_labor_force': row['civ_labor_force'],
      'employed': row['employed'],
      'unemployed': row['unemployed'],
      'unemployed': row['unemployed_rate']
    })
  # Update headers to allow CORS
  # Better would be to use flask-cors
  headers = Headers()
  headers.add('Access-Control-Allow-Origin', '*')
  headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET')
  headers.add('Access-Control-Allow-Headers', 'Content-Type')
  headers.add('Access-Control-Max-Age', '300')
  resp = make_response(
    jsonify(
      area=area,
      county=county,
      state=state,
      data=data
    )
  )
  resp.headers = headers
  return resp
```