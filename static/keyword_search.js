console.log('hello')

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






  // d3.select('#keyword_result').





  // updateChart(currentText);
});
