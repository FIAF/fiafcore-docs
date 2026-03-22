
async function drawPage(data) {


  // // okay drop down to subject data.
  // console.log('@@@', data.length)

  // console.log('@@@', resource)


  // let subject_data = data.find(item => item['@id'] === resource);

  // console.log('@@@', subject_data)


  d3.selectAll(".instep_1")
    .append("svg")
    .attr('class', "instep_1_svg")
    .attr("width", 50)
    .attr("height", 10);
  d3.selectAll(".instep_1_svg").append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 800)
    .attr("height", 400)
    .attr("fill", "white");

  d3.selectAll(".instep_1_svg").append("line")
    .attr("x1", 40)
    .attr("y1", 5)
    .attr("x2", 50)
    .attr("y2", 5)
    .attr("stroke", "black")
    .attr("stroke-width", 1);

  d3.selectAll(".instep_1_svg").append("line")
    .attr("x1", 40)
    .attr("y1", 0)
    .attr("x2", 40)
    .attr("y2", 5)
    .attr("stroke", "black")
    .attr("stroke-width", 1);

  // # add a line, it should be from last 50, top to middle down

  // // primary svg.

  d3.selectAll(".instep_3")
    .append("svg")
    .attr('class', "instep_3_svg")
    .attr("width", 100)
    .attr("height", 10);
  d3.selectAll(".instep_3_svg").append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 800)
    .attr("height", 400)
    .attr("fill", "white");



  d3.selectAll(".instep_3_svg").append("line")
    .attr("x1", 40+50)
    .attr("y1", 5)
    .attr("x2", 50+50)
    .attr("y2", 5)
    .attr("stroke", "black")
    .attr("stroke-width", 1);

  d3.selectAll(".instep_3_svg").append("line")
    .attr("x1", 40+50)
    .attr("y1", 0)
    .attr("x2", 40+50)
    .attr("y2", 5)
    .attr("stroke", "black")
    .attr("stroke-width", 1);



  d3.selectAll(".instep_5")
    .append("svg")
    .attr('class', "instep_5_svg")
    .attr("width", 150)
    .attr("height", 10);
  d3.selectAll(".instep_5_svg").append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 800)
    .attr("height", 400)
    .attr("fill", "white");


  d3.selectAll(".instep_5_svg").append("line")
    .attr("x1", 40+100)
    .attr("y1", 5)
    .attr("x2", 50+100)
    .attr("y2", 5)
    .attr("stroke", "black")
    .attr("stroke-width", 1);

  d3.selectAll(".instep_5_svg").append("line")
    .attr("x1", 40+100)
    .attr("y1", 0)
    .attr("x2", 40+100)
    .attr("y2", 5)
    .attr("stroke", "black")
    .attr("stroke-width", 1);




  // okay can we do a select all on all the line boxes, and draw lines!
  // things we know, anything low, has a parent, which instepped by 1

  // // title.

  // svg.append('text')
  //   .text(subject_data['http://www.w3.org/2000/01/rdf-schema#label'][0]['@value'])
  //   .attr('x', 0).attr('y', 100)
  //   .attr('class', 'title')

  // // initial line under title.

  // // svg.append("line")
  // //   .attr("x1", 0)
  // //   .attr("y1", 100+10)
  // //   .attr("x2", 40)
  // //   .attr("y2", 100+10)
  // //   .attr("stroke", "black")
  // //   .attr("stroke-width", 1);

  // // inital hookline.

  // svg.append("line")
  //   .attr("x1", 10)
  //   .attr("y1", 100+10)
  //   .attr("x2", 10)
  //   .attr("y2", 150+10)
  //   .attr("stroke", "black")
  //   .attr("stroke-width", 1);

  // svg.append("line")
  //   .attr("x1", 10)
  //   .attr("y1", 150+10)
  //   .attr("x2", 20)
  //   .attr("y2", 150+10)
  //   .attr("stroke", "black")
  //   .attr("stroke-width", 1);




  // // !!! Just worry about text placement for now
  // // example, identifier is 1 unit Y and default instep x
  // // actually identfiier is 1 unit y and another default instep x


  // svg.append('text')
  //   .text('identifier')
  //   .attr('x', 20+5).attr('y', 150+10)

  // svg.append('text')
  //   .text(subject_data['@id'].split('/').pop())
  //   .attr('x', 20+5+100).attr('y', 150+10)
  //   .on('click', function (k, d) {
  //      window.location.href = subject_data['@id'].split('/').pop();
  //    })

  // svg.append('text')
  //   .text('type')
  //   .attr('x', 20+5).attr('y', 150+10+40)

  // svg.append('text')
  //   .text(subject_data['@type'])
  //   .attr('x', 20+5+100).attr('y', 150+10+40)
  //   .on('click', function (k, d) {
  //      window.location.href = subject_data['@id'].split('/').pop();
  //    })





  // // line goes here

  // // console.log(data)

}

drawPage(data, resource)
