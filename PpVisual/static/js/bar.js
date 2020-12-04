function getLabelBar(AppLabelData,CaterData) {
	console.log("A",AppLabelData)
	console.log("B",CaterData)
	var data_json=[
    {
        "categorie": "隐私介绍",
        "values": [
            {
                "label": 0,
                "value": AppLabelData.label_0 ,
                "rate": "同类型app标签"
            },
            {
                "label": 0,
                "value": CaterData.label_0,
                "rate": "app自身标签"
            }
        ]
    },
    {
        "categorie": "第一方收集信息和使用",
        "values": [
            {
                "label": 1,
                "value": AppLabelData.label_1 ,
                "rate": "同类型app标签"
            },
            {
                "label": 1,
                "value": CaterData.label_1,
                "rate": "app自身标签"
            }
        ]
    },
    {
        "categorie": "Cookies以及相似技术",
        "values": [
            {
                "label": 2,
                "value": AppLabelData.label_2,
                "rate": "同类型app标签"
            },
            {
                "label": 2,
                "value": CaterData.label_2,
                "rate": "app自身标签"
            }
        ]
    },
    {
        "categorie": "第三方收集和分享数据",
        "values": [
            {
                "label": 3,
                "value": AppLabelData.label_3,
                "rate": "同类型app标签"
            },
            {
                "label": 3,
                "value": CaterData.label_3,
                "rate": "app自身标签"
            }
        ]
    },
    {
        "categorie": "用户选项及权利",
        "values": [
            {
                "label": 4,
                "value":AppLabelData.label_4,
                "rate": "同类型app标签"
            },
            {
                "label": 4,
                "value": CaterData.label_4,
                "rate": "app自身标签"
            }
        ]
    },
    {
        "categorie": "数据安全",
        "values": [
            {
                "label": 5,
                "value": AppLabelData.label_5,
                "rate": "同类型app标签"
            },
            {
                "label": 5,
                "value": CaterData.label_5,
                "rate": "app自身标签"
            }
        ]
    },
	{
	    "categorie": "数据保留",
	    "values": [
	        {
                "label": 6,
	            "value":AppLabelData.label_6,
	            "rate": "同类型app标签"
	        },
	        {
                "label": 6,
	            "value": CaterData.label_6,
	            "rate": "app自身标签"
	        }
	    ]
	},
	{
	    "categorie": "国际数据存储及转移",
	    "values": [
	        {
                "label": 7,
	            "value": AppLabelData.label_7,
	            "rate": "同类型app标签"
	        },
	        {
                "label": 7,
	            "value": CaterData.label_7,
	            "rate": "app自身标签"
	        }
	    ]
	},
	{
	    "categorie": "特殊人群",
	    "values": [
	        {
                "label": 8,
	            "value": AppLabelData.label_8,
	            "rate": "同类型app标签"
	        },
	        {
                "label": 8,
	            "value": CaterData.label_8,
	            "rate": "app自身标签"
	        }
	    ]
	},
	{
	    "categorie": "隐私政策修改",
	    "values": [
	        {
                "label": 9,
	            "value": AppLabelData.label_9,
	            "rate": "同类型app标签"
	        },
	        {
                "label": 9,
	            "value":CaterData.label_9,
	            "rate": "app自身标签"
	        }
	    ]
	},
		{
			"categorie": "隐私政策联系信息",
			"values": [
				{
					"label": 10,
					"value": AppLabelData.label_10,
					"rate": "同类型app标签"
				},
				{
					"label": 10,
					"value": CaterData.label_10,
					"rate": "app自身标签"
				}
			]
		}
		];
      var margin = {top: 10, right: 20, bottom: 180, left: 80},
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    var x0 = d3.scale.ordinal()
        .rangeRoundBands([0, width], 0.5);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x0)
        .tickSize(0)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");
    var color = new Array("#ffd2cc", "#1982c4", "#ffca3a", "#9c89b8", "#2ec4b6", "#ff595e", "#6a4c93", "#118ab2", "#83c5be", "#f0a6ca", "#9a8c98");
    var svg = d3.select('div#bar').append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var categoriesNames = data_json.map(function(d) { return d.categorie; });
        var rateNames = data_json[0].values.map(function(d) { return d.rate; });
        // console.log(rateNames);

        x0.domain(categoriesNames);
        x1.domain(rateNames).rangeRoundBands([0, x0.rangeBand()]);
        y.domain([0, d3.max(data_json, function(categorie) { return d3.max(categorie.values, function(d) { return d.value; }); })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-40)")
            .attr("fill","white");

        svg.append("g")
            .attr("class", "y axis")
            .attr("fill","white")
            .style('opacity','0')
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .style('font-weight','bold');

        svg.select('.y').transition().duration(100).delay(1600).style('opacity','1');
        var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d,i) {
                console.log(d.data);
                return "<strong style='color: white'>"+(d.rate)+"</strong> <span style='color:red'>" + d.value + "</span>";
            });
        svg.call(tip);
        var slice = svg.selectAll(".slice")
            .data(data_json)
            .enter().append("g")
            .attr("class", "g")
            .attr("transform",function(d) { return "translate(" + x0(d.categorie) + ",0)"; });



        slice.selectAll("rect")
            .data(function(d) { return d.values; })
            .enter().append("rect")
            .attr("class","rect")
            .attr("width", x1.rangeBand())
            .attr("x", function(d) { return x1(d.rate); })
            // .attr("x", function(d) { return x1(d.rate); })
            .style("fill", function (d, i) {
                var colo=color[d.label];
                return colo;
            })
            .attr("y", function(d) { return y(0); })
            .attr("height", function(d) { return height - y(0); })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

        slice.selectAll("rect")
            .transition()
            .delay(function (d) {return Math.random()*1000;})
            .duration(1000)
            .attr("y", function(d) { return y(d.value); })
            .attr("height", function(d) { return height - y(d.value); });
}