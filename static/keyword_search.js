console.log('hello')

function display_results(data) {
  console.log('@@@')
  console.log(data.length)
}

d3.select("#keyword_result")
    .append("svg")
    .attr("id", "keyword_canvas")
    .attr("width", '100%')
    .attr("height", 500)
    .style("background-color", "#FFE5B4");

d3.select("#keyword_text").on("change", function (event) {

  let keyword_text = d3.select(this).property("value");
  let keyword_type = d3.select("#keyword_type").property("value");
  console.log('@@@', keyword_type, keyword_text)

  let url = 'https://data.fiafcore.org';
  let sparqlQuery = `
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    select ?institution (count(?item) as ?items)
    where {
      ?item <https://dev.fiafcore.org/hasHoldingInstitution> ?i .
      ?i rdfs:label ?institution
      } group by ?institution
  `;

  // prefix fiaf: <https://dev.fiafcore.org/>
  // prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  // prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  // select ?work ?label where {
  //   ?work rdf:type/rdfs:subClassOf* fiaf:Work .
  //   ?work rdfs:label ?label .
  //   filter(contains(lcase(str(?label)), "lunch"))
  // } limit 100

  let body = new URLSearchParams();
  body.append('query', sparqlQuery);

  fetch(url, {
    method: 'POST',
    headers: {
      'Accept': 'application/sparql-results+json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: body
  })
  .then(response => response.json())
  .then(data => console.log(data['results']['bindings']))
  .catch(error => console.error('Erreur:', error));

});
