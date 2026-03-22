
async function drawNodes(data) {

  const svg = d3.select("#page")
    .append("svg")
    .attr("width", 800)
    .attr("height", 400);

  svg.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 800)
    .attr("height", 400)
    .attr("fill", "lightblue");

  console.log(data)

}
drawNodes(data)
