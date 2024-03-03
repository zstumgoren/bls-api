
Create an API Gateway and API Config using OpenAPI/Swagger spec

- https://cloud.google.com/api-gateway/docs/creating-api-config

Create new service account.

> Below step from [Creating and deploying an API](https://cloud.google.com/api-gateway/docs/configure-dev-en)]

```
gcloud iam service-accounts add-iam-policy-binding SERVICE_ACCOUNT_EMAIL \
  --member user:USER_EMAIL \
  --role roles/iam.serviceAccountUser
```


List existing API configs, if any.

```
gcloud api-gateway api-configs list --project=hs-research-tumgoren

# or for a specific project, as below

gcloud api-gateway api-configs list --api=bls --project=hs-research-tumgoren --format="table(name, labels)"
```

Describe a config.

```
gcloud api-gateway api-configs describe bls-api-config --api=bls --project=hs-research-tumgoren
```

Create an API Config.

```
gcloud api-gateway api-configs create CONFIG_ID \
  --api=API_ID --openapi-spec=API_DEFINITION \
  --project=PROJECT_ID --backend-auth-service-account=SERVICE_ACCOUNT_EMAIL

# Note the CONFIG_ID must be different than any pre-existing!!
# E.g., if you already had bls-api-config, you can't use it again!
gcloud api-gateway api-configs create bls-api-config-v1 \
  --api=bls --openapi-spec=api.yaml \
  --project=hs-research-tumgoren \
  --backend-auth-service-account=hs-research-tumgoren@appspot.gserviceaccount.com
```

You cannot [update an API config][]. You must upload a modified version of
the config (ie the local yaml file) using a new API config name. And
then you can delete the pre-existing one.

[update an API config]: https://cloud.google.com/api-gateway/docs/creating-api-config#updating-an-api-config

To delete a pre-existing API config (after uploading a new):

```
gcloud api-gateway api-configs delete CONFIG_ID --api=API_ID --project=PROJECT_ID

gcloud api-gateway api-configs delete bls-api-config --api=bls --project=hs-research-tumgoren
```
