function renderSearchResults(data) {
    console.log(data);
    const resultsDiv = document.querySelector('#search-results');
    const area = data.area;
    const vlSpec = {
      "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
      "description": `Unemployment rate: ${area}`,
      "data": {"values": data.data},
      "mark": "line",
      "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "unemployed_rate", "type": "quantitative"}
      }
    }
    vegaEmbed('#vis', vlSpec);
  };

// Use currying to configure onsubmit callback function that targets 
// a particular API endpoint 
function submitSearch(url) {
    return (event) => {
    // Prevent normal form action of changing page URL based on form values;
    event.preventDefault(); 
    const county = document.querySelector('#county').value;
    const state = document.querySelector('#state').value;
    console.log(`${county}, ${state}`);
    const query_url = `${url}?county=${county}&state=${state}`;
    console.log(query_url);
    const data = fetch(query_url)
      .then(response => response.json())
      .then(data => {
        renderSearchResults(data);
        //console.log(data)
      });
    };
  };