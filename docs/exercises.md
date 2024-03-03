# Exercises

We have a very basic data visualization at this point.

But there is so much more we could do to add some polish to this simple little chart, especially to improve its style, information content, and overall ease of use.

Below are some exercises to incrementally improve our visualization.

## Show rates on hover

The graphic currently shows a line chart based on monthly figures for the last 14 months.

Wouldn't it be snazzy if a user could hover on a point in the line chart and see the unemployment rate for that month?

Vega-Lite makes it easy to add helpful little touches such as this.

Dig through their documentation to see if you can figure out how to display data points on hover.

## Add fuzzy search

The use of a web form requires a user to know they must include the word "County" in their search. 

And unfortunately, if you carefully review the BLS unemployment data over on BigQuery, you'll notice that not all counties end with the word "County".

Take a minute to head back over to BigQuery on Google Cloud Platform.

- Craft a `SELECT DISTINCT` SQL query for all counties in California.
- Review the results carefully. Notice any counties that don't quite fit the pattern?

There are a number of ways we could handle this. One might be to fix the source data in BigQuery.

Or you could provide the user with "fuzzy search" -- basically the ability to begin typing a county name, and then have a dynamically populated list of counties from which they can choose.

This will free them from having to type the name of a county perfectly, and it will free you from having to potentially standardize all county names.

There's a nifty Javascript library called [Fuse.js](https://www.fusejs.io/) that provides fuzzy search.

Try updating the code to replace the current web form with a fuzzy search using Fuse.js.


## Add dynamic text

A line chart is all well and good, but a real news graphic typically provides some sort of analysis or broader interpretation of the data for readers.

For example, a headline might be dynamically generated, in Mad Libs style, that says unemployment went up (or down) for a given county based on the actual data.

Try updating your code to include some dynamic text. There are a a few ways to handle this.

You could update the API code in your Cloud Function to perform some calculation and then include the result in the JSON sent to the browser. You could even generate the full text to be displayed in the browser as part of the API response. It then becomes a simple matter of plugging that content into the appropriate spot on the page.

An alternative approach would be to write custom Javascript that performs the calculation in the browser, after the unemployment rates are returned by the API.

With this small amount of data, either approach is fine.

Choose a strategy and see if you can add some dynamic text (e.g. a headline, caption, or both).

You should start this exercise, by the way, by first deciding what type of information you're trying to communicate to the reader.

Here are some initial ideas:

- Did the unemployment rate go up or down between this month and the prior month?
- How much has the unemployment rate changed over the last 14 months?
- What is the average unemployment rate for the 14-month period?

