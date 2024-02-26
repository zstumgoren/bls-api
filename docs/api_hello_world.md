## Hello API

First off, what the heck is an API? 

We hear the term all the time and it's been around many years. 

API is an acronym for Application Programming Interface and in it denotes a higher-level code interface that provides a simpler means of access to more complex underlying functionality, data, or both. 

The goal is to make life easier for those using the API -- i.e. the "callers".

In a web context, APIs typically are a web application that allow you to flexibly request data based on a set of specifications.

For example, if we wanted to create a web app that allows users to look up unemployment data by county and state, it would make sense to create an underlying API that accepts county and state parameters (e.g. submitted to the API using a web form). The plumbing -- how the API goes about accessing data, and where that data is stored -- is something the user doesn't need to worry about.

There are many tools and strategies for creating web APIs, and one of the easiest options these days is the use of functions in the cloud. 

These are precisely what they sound like -- typically a function, written in a language such as Python, that respond to web requests and return data.

A variety of cloud platforms such as Amazon Web Services and Google Cloud Platform (GCP) provide cloud functions.

For this tutorial, we'll use  GCP Cloud Functions, but just be aware that others offer similar functionality (e.g. AWS Lambdas).

Before we get to the fancy stuff, we'll start by simply creating a basic API to get a feel for Google Cloud Functions.

We'll then move on to a more sophisticated API that can be used in our data visualization app.

## Cloud Functions - hello world

GCP provides the ability to easily create an API "endpoint" using basic Python code (or node JS or a variety of other languages).

How do we create APIs using Google Cloud Functions?

> Make sure you've completed the steps in the [setup docs](docs/setup.md)

Go to the Cloud Functions Dashboard. You can locate the dashboard using the search bar at the top of the GCP Console:

![gcp console search for cloud functions](../static/img/gcp_search.png)

Select `Cloud Functions` and you should be taken to the dashboard.

Click `CREATE FUNCTION` at the top of the page.

Create a `hello_world` function with the following settings:

- Environment: `2nd gen`
- Function name: `hello_world`
- Region: `us-central1 (Iowa)`
- Trigger type: `HTTPS`
- Authentication: `Allow unauthenticated invocations`

It should look like the below:

![hello world cloud function config](../static/img/hello_world_function_config.png)

Click `Next`.

You should now be on the source code editor screen. You may notice the default starter code is using `node.JS`.

Let's go ahead and change this to a recent version of Python (e.g. 3.11) using the `Runtime` drop-down menu.

![select python runtime](../static/img/select_python_runtime.png)

Once you've selected `Python 3.11`, the example code should update to our newly selected language.

It provides a handy little `hello_http` function for us.

![hello http function](../static/img/hello_http.png)

This code may seem complex, so let's go through a few important points:

- The `hello_http(request)` is the so-called `Entry point` function. This is the top-level function that will be called when a web request is made to the URL for our function. The function is "annotated" with what's known as a "decorator" -- basically another function that adds special functionality - called `@functions_framework.http`. This bit of code "wraps" our entry point function and enables it to run in this particular cloud environment. For the curious, gory details are [here](https://github.com/GoogleCloudPlatform/functions-framework-python).
- The function is using a Python web framework called Flask, which expects a `request` argument, which will contain details about the web request when it is made.
- Our code is technically stored in a file called `main.py` (see area to the left of the code editor). There is also a `requirements.txt`, which you can use to add other software libraries required by the function.
- The code logic itself is fairly straightforward - if you call the API, it will simply return the phrase `Hello World!`. Or if you provide a `name=SomeName` parameter when calling the URL, it will pluck that parameter from the URL and substitute the name in the return message: `Hello SomeName`.

Let's click the blue `DEPLOY` at page bottom and test our function. It'll take a minute or two to deploy...

## Triggering our function

While the cloud function deploys, you should be taken to a new screen with a series of tabs. 

These tabs provide details about your cloud function and its configuration, along with the "endpoint", or URL that can be used to call the function.

![hello function config](../static/img/hello_func_config.png)

If you see a check mark in a green circle next to your function's name, it's ready to be called.

Click the URL and you should see a simple `Hello World!` message.

Congrats! You just deployed your first API!! 

But wait, it gets better.

As mentioned earlier, you can also supply a URL parameter by adding a `?` to the end of the URL, followed by `name=SomeName`. Try tacking that on to the end of the URL and replace `SomeName` with your own name.

In my case, the URL looks like this:

```
https://us-central1-hs-research-tumgoren.cloudfunctions.net/hello_world?name=Serdar
```

You should get back a different message this time using your own name. In my case, that's `Hello Serdar!`

You've successfully set up a basic API URL or, more formally, an "[endpoint](https://en.wikipedia.org/wiki/Web_API#Endpoints)".

We're now ready to get a bit fancier by creating an endpoint that queries data stored on the cloud.

Head over to the [BigQuery docs](bigquery.md) to learn about that service and how to connect it with your API to return unemployment data.