import json
from google.cloud import bigquery

client = bigquery.Client()

def bls_county_data(request):
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    if request.args and 'county' in request.args and 'state' in request.args:
        # NOTE: You could do additional sanity checking and standardization here
        # on incoming data here
        county = request.args.get('county')
        state = request.args.get('state').strip().upper()
    else:
        return ('You must supply the county and state URL parameters', 400, headers)
    query_template = """
       SELECT *
       FROM `hs-research-tumgoren.bls.unemployment`
       WHERE `county` = '{}' and `state` = '{}'
    ;
    """
    query = query_template.format(county, state)
    query_job = client.query(query)
    payload = {'data':[]}
    for row in query_job:
        payload.update({
            'area': row['area'],
            'county': row['county'],
            'state': row['state'],
        })
        payload['data'].append({
          'month_abbrev': row['month_name'],
          'month': row['month'],
          'date': row['date'].strftime("%Y-%m-%d"),
          'year': row['year'],
          'civ_labor_force': row['civ_labor_force'],
          'employed': row['employed'],
          'unemployed': row['unemployed'],
          'unemployed_rate': row['unemployed_rate'],
        })
    return (json.dumps(payload), 200, headers)
