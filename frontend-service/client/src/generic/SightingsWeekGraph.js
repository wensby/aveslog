import React, { useState, useEffect, useRef } from 'react';
import './SightingsWeekGraph.scss';
var d3 = require("d3");

const getWeek = date => {
  var onejan = new Date(date.getFullYear(), 0, 1);
  return Math.ceil((((date - onejan) / 86400000) + onejan.getDay() + 1) / 7);
}

const SightingsWeekGraph = ({ sightings }) => {
  const [data, setData] = useState([]);
  const ref = useRef();

  useEffect(() => {
    const newData = [];
    for (var i = 1; i <= 52; i++) {
      const iConst = i;
      const count = sightings
        .map(s => getWeek(new Date(s.date)))
        .filter(week => week === iConst).length;
      newData.push({ week: i, value: count });
    }
    newData.push({week: 52, value: 0});
    newData.push({week: 1, value: 0});
    setData(newData);
  }, [sightings]);

  useEffect(() => {
    const xScale = d3.scaleLinear()
      .domain([1, 52])
      .range([10, 390]);
    var yScale = d3.scaleLinear()
      .domain([0, Math.max(...data.map(d => d.value))])
      .range([60, 20]);
    const svg = d3.select(ref.current);
    svg.selectAll('*').remove();
    const axisGenerator = d3.axisBottom(xScale)
      .ticks(26);
    svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0,60)")
      .call(axisGenerator);
    svg.append("path")
      .datum(data)
      .attr("fill", "#EE6352")
      .attr("stroke", "#EE6352")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(d => xScale(d.week))
        .y(d => yScale(d.value))
      );
    const texts = svg.selectAll(".myTexts")
      .data(data)
      .enter()
      .append("text");
    texts.attr('class', 'label')
      .attr("x", d => xScale(d.week) - 3)
      .attr("y", d => yScale(d.value) - 5)
      .text(d => d.value ? d.value : '');
  }, [data]);

  return (
    <svg viewBox="0 0 400 80" ref={ref}></svg>
  );
}


export { SightingsWeekGraph };
