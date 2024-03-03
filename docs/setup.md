# Setup

## Get the code

Clone this repository:

```bash
git clone git@github.com:zstumgoren/bls-api.git
```

## Set up Google Cloud Platform

> Below steps are based on [these docs](https://cloud.google.com/functions/docs/console-quickstart)

* Create Google Cloud Platform account
* Create a Google Cloud Project called `bls-data-viz-YOUR_NAME>`, substituting your first name where it says `YOUR_NAME`. If you get an error saying the name is already taken, try adding your family name as well.
* Make sure billing is enabled for your project
* Enable APIs
  * Cloud Functions
  * Cloud Build
  * Artifact Registry
  * Cloud Run
  * Logging
  * Pub/Sub APIs
  * BigQuery