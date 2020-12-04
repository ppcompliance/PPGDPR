(function () {
    var margin = {top: 60, right: 30, bottom: 30, left: 60},
        width = 360 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;
    var svg = d3.select("#tsne").append("svg")
        .attr("width",width + margin.left + margin.right)
        .attr("height",height + margin.top + margin.bottom)
        .append("g").attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
    d3.csv("F://PpVisual//static//data//tsne.csv", function (data) {
        // console.log(data);
        var d_extent_x = d3.extent(data, data => +data.x),
            d_extent_y = d3.extent(data, data => +data.y);
        // console.log(d_extent_x);
        var x =d3.scale.linear().domain(d_extent_x).range([0,width]);
        // svg.append("g")
        // 		.attr("transform", "translate(0," + height + ")")
        // 		.call(d3.svg.axis().scale(x));
        var y = d3.scale.linear()
            .domain(d_extent_y)
            .range([ height, 0]);
        // svg.append("g")
        // 		.call(d3.svg.axis(y).orient("left"));
        svg.append('g')
            .selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.x); } )
            .attr("cy", function (d) { return y(d.y); } )
            .attr("r", 3)
            .style("fill", "#69b3a2")
            .style("stroke",'#1e407b')
            .style("stroke-width",2)
            .style("opacity",0.6);


    });

})();