// Use currying to configure onsubmit callback function that 
// accepts url and optional API key
function submitSearch(url, apiKey) {
  return (event) => {
  // Prevent normal form action of changing page URL based on form values;
  event.preventDefault();
  const county = document.querySelector('#county').value;
  const state = document.querySelector('#state').value;
  console.log(`${county}, ${state}`);
  console.log(`API Key: ${apiKey}`)
  let query_url = new URL(url);
  query_url.searchParams.set('county', county);
  query_url.searchParams.set('state', state);
  if (typeof apiKey !== 'undefined') {
    query_url.searchParams.set('key', apiKey);
  }
  console.log(query_url.toString());
  const data = fetch(query_url)
    .then(response => response.json())
    .then(data => {
      renderSearchResults(data);
    });
  };
};

function renderSearchResults(data) {

    const resultsDiv = document.querySelector('#search-results');
    const area = data.area;
    const vlSpec = {
      $schema: "https://vega.github.io/schema/vega-lite/v5.json",
      description: `Unemployment rate: ${area}`,
      data: {values: data.data},
      mark: "line",
      encoding: {
        x: {field: "date", type: "temporal", timeUnit: "yearmonth"},
        y: {field: "unemployed", type: "quantitative"}
      }
    };
    vegaEmbed('#vis', vlSpec);
  };