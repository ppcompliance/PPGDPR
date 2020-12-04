(function(){
	var margin = {top: 20, right: 20, bottom: 100, left: 50},
	             width = 690 - margin.left - margin.right,
	             height = 240 - margin.top - margin.bottom;
	var svg = d3.select("div#pptext").append("svg")
				             .attr("width", width + margin.left + margin.right)
				             .attr("height", height + margin.top + margin.bottom)
				              .append("g")
				            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	var div = d3.select("div#pptext").append("div")   
	    .attr("class", "tooltip")               
	    .style("opacity", 0);
	var parseDate = d3.time.format("%Y-%m-%d").parse;
	var formatDate = d3.time.format("%y");
	var formatDate_m = d3.time.format("%m");
	// var x = d3.time.scale().range([0, width]);
	  
	// var y = d3.scale.linear().range([height,0]);
	  
	// var xAxis = d3.svg.axis()
	//               .scale(x)
	//              .orient("bottom")
	//              .tickFormat(d3.time.format("%y.%m"));
	 
	// var yAxis = d3.svg.axis()
	//              .scale(y)
	// 			 .tickFormat(d3.format("s"))
	//              .orient("left");
	d3.csv("./data/9.csv", function(error, data){
		if(error){
			console.log(error);
		}
		var result=[];
		var rs=[];
		for(var i= 0;i<data.length;i++){
			date=data[i].date;
			close = data[i].number;
			rs.push(Number(close));
			var re ={}
			re.date = parseDate(date);
			re.number= (+close);
			// console.log(re);
			result.push(re)
		}
		console.log(rs);
		// data.forEach(function(d){
		// 	// console.log(d.date);
		// 	console.log(parseDate(d.date))
		// 	d.date =parseDate(d.date);
		// 	d.close = +d.number;
		// });
		// var prefix = d3.formatPrefix(1200);
		// console.log(prefix);
		var xScale  = d3.time.scale().domain(d3.extent(result,function(d){return ((d.date));})).range([0, width]);
		  
		var yScale  = d3.scale.linear().domain(d3.extent(result, function(d){return d.number;})).range([height,0]);
		var xAxis = d3.svg.axis()
		              .scale(xScale)
		             .orient("bottom")
		             .tickFormat(d3.time.format("%y.%m"));
		 
		var yAxis = d3.svg.axis()
		             .scale(yScale)
					 .tickFormat(d3.format("s"))
		             .orient("left");
		// x.domain(d3.extent(data,function(d){return ((d.date));}));
		// y.domain(d3.extent(data, function(d){return d.number;}));
		// var line = d3.svg.line()
		//                 .x(function(d) { return x((date)); })
		//                 .y(function(d) { return y(close); });
		var line = d3.svg.line().x(function(d){ return xScale(d.date)}).y(function(d){return yScale(d.number)})
		svg.append("g")
		                .attr("class", "x axis")
		                .attr("transform", "translate(0," + height + ")")
		                .call(xAxis)
						.style("font-size","10px")
						.selectAll("text")
						.style("text-anchor", "end")
						.attr("dx", "-.1em")
						.attr("dy", ".10em")
						.attr("transform", "rotate(-90)");
		svg.append("g")
		                .attr("class", "y axis")
		                .call(yAxis)
						.style("font-size","10px")
		                .append("text")
		                .attr("transform", "rotate(0)")
		                .attr("y", -15)
		                .attr("x", 25)
		                .attr("dy", ".71em")
						.style("font-size","10px")
		                .style("text-anchor", "end")
		                .text("文本长度");
		//定义纵轴网格线
		var yInner = d3.svg.axis()
		                .scale(yScale)
		                .tickSize(-width,0,0)
		                .tickFormat("")
		                .orient("left")
		                .ticks(5);
		        //添加纵轴网格线
		var yInnerBar=svg.append("g")
		                .attr("class", "inner_line")
		                .attr("transform", "translate(0,-25)")
		                .call(yInner);
		svg.append("path")
		                .datum(result)
		                .attr("class", "line")
		                .attr("d", line(result))
		                .attr("opacity", 10)
		                .transition()
		                .duration(2000)
		                .attr("opacity", 10);
		 var points = svg.selectAll(".MyCircle")
		                .data(result)
		                .enter()
		                .append("circle")
		                .attr("class","MyCircle")
		                .attr("transform","translate(0,0)")
						.on("mouseover", function(d) {      
						            div.transition()        
						                .duration(200)      
						                .style("opacity", .9);      
						            div .html(formatDate(d.date)+"年"+formatDate_m(d.date)+"月" + "<br/>"  +"文本长度："+ d.number)  
						                .style("left", (d3.event.pageX) + "px")     
						                .style("top", (d3.event.pageY - 28) + "px");    
						            })                  
						        .on("mouseout", function(d) {       
						            div.transition()        
						                .duration(500)      
						                .style("opacity", 0);   
						        })
		                .attr("r", 3)
		                .attr("opacity", 0)
		                .transition()
		                .duration(200)
		                .attr("cx", function(d){ return xScale(d.date); })
		                .attr("opacity", 1)
		                .attr("cy", function(d){ return yScale(d.number); });
						
	
	       
	});
})();